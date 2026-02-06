#!/usr/bin/env python3
"""
Gerrit Weekly Activity Monitor
Monitors Gerrit repository for weekly activities and posts updates to Slack.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GerritMonitor:
    """Monitor Gerrit repository for changes and activities."""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the Gerrit monitor with configuration."""
        self.config = self._load_config(config_path)
        self.gerrit_url = self.config.get('gerrit_url', 'https://gerrit.openbmc.org')
        self.project = self.config.get('project', 'openbmc/webui-vue')
        self.check_days = self.config.get('check_days', 7)
        self.max_results = self.config.get('max_results', 100)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            return {}
    
    def fetch_changes(self) -> List[Dict]:
        """Fetch changes from Gerrit API for the specified time period."""
        # Calculate the date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=self.check_days)
        
        # Format dates for Gerrit query (YYYY-MM-DD)
        start_date_str = start_date.strftime('%Y-%m-%d')
        
        # Build Gerrit API query
        # Query format: project:PROJECT after:DATE
        query = f"project:{self.project} after:{start_date_str}"
        
        # Gerrit REST API endpoint
        api_url = f"{self.gerrit_url}/changes/"
        
        params = {
            'q': query,
            'n': self.max_results,
            'o': ['CURRENT_REVISION', 'DETAILED_ACCOUNTS', 'MESSAGES']
        }
        
        try:
            logger.info(f"Fetching changes from Gerrit: {query}")
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Gerrit prepends ")]}'" to JSON responses for security
            content = response.text
            if content.startswith(")]}'"):
                content = content[4:]
            
            changes = json.loads(content)
            logger.info(f"Found {len(changes)} changes")
            return changes
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching changes from Gerrit: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gerrit response: {e}")
            return []
    
    def categorize_changes(self, changes: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize changes by their status."""
        categorized = {
            'merged': [],
            'open': [],
            'abandoned': [],
            'work_in_progress': []
        }
        
        for change in changes:
            status = change.get('status', '').lower()
            
            change_info = {
                'subject': change.get('subject', 'No subject'),
                'owner': change.get('owner', {}).get('name', 'Unknown'),
                'number': change.get('_number', 0),
                'url': f"{self.gerrit_url}/c/{change.get('_number', 0)}",
                'updated': change.get('updated', ''),
                'insertions': change.get('insertions', 0),
                'deletions': change.get('deletions', 0),
                'status': status
            }
            
            if status == 'merged':
                categorized['merged'].append(change_info)
            elif status == 'new':
                if change.get('work_in_progress', False):
                    categorized['work_in_progress'].append(change_info)
                else:
                    categorized['open'].append(change_info)
            elif status == 'abandoned':
                categorized['abandoned'].append(change_info)
        
        return categorized


class SlackNotifier:
    """Send notifications to Slack via webhook."""
    
    def __init__(self, webhook_url: str):
        """Initialize Slack notifier with webhook URL."""
        self.webhook_url = webhook_url
    
    def format_message(self, categorized_changes: Dict[str, List[Dict]], 
                      project: str, days: int) -> Dict:
        """Format changes into a Slack message."""
        total_changes = sum(len(changes) for changes in categorized_changes.values())
        
        # Build message blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Weekly Gerrit Activity Report",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Project:* `{project}`\n*Period:* Last {days} days\n*Total Changes:* {total_changes}"
                }
            },
            {
                "type": "divider"
            }
        ]
        
        # Add merged changes
        if categorized_changes['merged']:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*✅ Merged Changes ({len(categorized_changes['merged'])})*"
                }
            })
            
            for change in categorized_changes['merged'][:10]:  # Limit to 10
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_ (+{change['insertions']}/-{change['deletions']})"
                    }
                })
            
            if len(categorized_changes['merged']) > 10:
                blocks.append({
                    "type": "context",
                    "elements": [{
                        "type": "mrkdwn",
                        "text": f"_...and {len(categorized_changes['merged']) - 10} more merged changes_"
                    }]
                })
        
        # Add open changes
        if categorized_changes['open']:
            blocks.append({
                "type": "divider"
            })
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🔍 Open Changes Awaiting Review ({len(categorized_changes['open'])})*"
                }
            })
            
            for change in categorized_changes['open'][:10]:  # Limit to 10
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                    }
                })
            
            if len(categorized_changes['open']) > 10:
                blocks.append({
                    "type": "context",
                    "elements": [{
                        "type": "mrkdwn",
                        "text": f"_...and {len(categorized_changes['open']) - 10} more open changes_"
                    }]
                })
        
        # Add work in progress changes
        if categorized_changes['work_in_progress']:
            blocks.append({
                "type": "divider"
            })
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🚧 Work In Progress ({len(categorized_changes['work_in_progress'])})*"
                }
            })
            
            for change in categorized_changes['work_in_progress'][:5]:  # Limit to 5
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                    }
                })
        
        # Add abandoned changes
        if categorized_changes['abandoned']:
            blocks.append({
                "type": "divider"
            })
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*❌ Abandoned Changes ({len(categorized_changes['abandoned'])})*"
                }
            })
            
            for change in categorized_changes['abandoned'][:5]:  # Limit to 5
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                    }
                })
        
        # Add footer
        blocks.append({
            "type": "divider"
        })
        blocks.append({
            "type": "context",
            "elements": [{
                "type": "mrkdwn",
                "text": f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
            }]
        })
        
        return {"blocks": blocks}
    
    def send_message(self, message: Dict) -> bool:
        """Send message to Slack webhook."""
        try:
            logger.info("Sending message to Slack")
            response = requests.post(
                self.webhook_url,
                json=message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            logger.info("Message sent successfully to Slack")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to Slack: {e}")
            return False


def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()
    
    # Get Slack webhook URL from environment
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    if not slack_webhook_url:
        logger.error("SLACK_WEBHOOK_URL environment variable not set")
        logger.error("Please set it in your .env file or environment")
        sys.exit(1)
    
    # Override config with environment variables if present
    config_overrides = {}
    if os.getenv('GERRIT_URL'):
        config_overrides['gerrit_url'] = os.getenv('GERRIT_URL')
    if os.getenv('PROJECT'):
        config_overrides['project'] = os.getenv('PROJECT')
    check_days_env = os.getenv('CHECK_DAYS')
    if check_days_env:
        config_overrides['check_days'] = int(check_days_env)
    
    # Initialize monitor
    monitor = GerritMonitor()
    
    # Apply environment overrides
    for key, value in config_overrides.items():
        setattr(monitor, key, value)
        monitor.config[key] = value
    
    logger.info(f"Monitoring project: {monitor.project}")
    logger.info(f"Checking last {monitor.check_days} days")
    
    # Fetch changes
    changes = monitor.fetch_changes()
    
    if not changes:
        logger.warning("No changes found or error fetching changes")
        # Still send a message to Slack indicating no activity
        notifier = SlackNotifier(slack_webhook_url)
        empty_message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📊 Weekly Gerrit Activity Report",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Project:* `{monitor.project}`\n*Period:* Last {monitor.check_days} days\n*Total Changes:* 0"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "No activity found in the specified period."
                    }
                }
            ]
        }
        notifier.send_message(empty_message)
        return
    
    # Categorize changes
    categorized = monitor.categorize_changes(changes)
    
    # Send to Slack
    notifier = SlackNotifier(slack_webhook_url)
    message = notifier.format_message(categorized, monitor.project, monitor.check_days)
    
    success = notifier.send_message(message)
    
    if success:
        logger.info("Weekly report sent successfully!")
    else:
        logger.error("Failed to send weekly report")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
