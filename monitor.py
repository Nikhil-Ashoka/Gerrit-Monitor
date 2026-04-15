#!/usr/bin/env python3
"""
Gerrit Daily Activity Monitor
Monitors Gerrit repository for daily activities and generates reports.
Can optionally post updates to Slack if webhook URL is provided.
Can optionally send email reports if SMTP settings are configured.
"""

import os
import sys
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
        
        # Support both old single-project and new multi-project config
        if 'projects' in self.config:
            self.projects = self.config['projects']
        else:
            # Backward compatibility: convert old format to new
            self.projects = [{
                'name': self.config.get('project', 'openbmc/webui-vue'),
                'check_days': self.config.get('check_days', 7),
                'max_results': self.config.get('max_results', 100)
            }]
        
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
    
    def fetch_changes_for_project(self, project_config: Dict) -> List[Dict]:
        """Fetch changes from Gerrit API for a specific project."""
        project_name = project_config['name']
        check_days = project_config.get('check_days', 7)
        max_results = project_config.get('max_results', 100)
        
        # Calculate the date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=check_days)
        
        # Format dates for Gerrit query (YYYY-MM-DD)
        start_date_str = start_date.strftime('%Y-%m-%d')
        
        # Build Gerrit API query
        # Query format: project:PROJECT after:DATE
        query = f"project:{project_name} after:{start_date_str}"
        
        # Gerrit REST API endpoint
        api_url = f"{self.gerrit_url}/changes/"
        
        params = {
            'q': query,
            'n': max_results,
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
            logger.info(f"Found {len(changes)} changes for {project_name}")
            return changes
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching changes from Gerrit for {project_name}: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gerrit response for {project_name}: {e}")
            return []
    
    def fetch_all_changes(self) -> Dict[str, List[Dict]]:
        """Fetch changes for all configured projects."""
        all_changes = {}
        for project_config in self.projects:
            project_name = project_config['name']
            changes = self.fetch_changes_for_project(project_config)
            all_changes[project_name] = changes
        return all_changes
    
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


class ReportGenerator:
    """Generate reports in various formats."""
    
    def generate_markdown_report(self, all_categorized_changes: Dict[str, Dict[str, List[Dict]]],
                                 projects_config: List[Dict], gerrit_url: str) -> str:
        """Generate a markdown report of the changes for multiple projects."""
        # Get current date for report
        report_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Calculate total changes across all projects
        total_changes = 0
        for categorized in all_categorized_changes.values():
            total_changes += sum(len(changes) for changes in categorized.values())
        
        report = []
        report.append("# 📊 Gerrit Activity Report\n")
        report.append(f"**Generated:** {report_date}\n")
        
        # Show different format based on number of projects
        if len(projects_config) > 1:
            # Multiple projects: show "Projects:" and "Total Changes:"
            project_names = ', '.join([p['name'] for p in projects_config])
            report.append(f"**Projects:** {project_names}\n")
            report.append(f"**Total Changes:** {total_changes}\n")
        else:
            # Single project: show "Project:" and "Changes:" (without "Total")
            project_name = projects_config[0]['name']
            report.append(f"**Project:** {project_name}\n")
            report.append(f"**Changes:** {total_changes}\n")
        
        report.append("\n---\n")
        
        # Generate report for each project
        for project_config in projects_config:
            project_name = project_config['name']
            days = project_config.get('check_days', 7)
            
            if project_name not in all_categorized_changes:
                continue
                
            categorized_changes = all_categorized_changes[project_name]
            project_total = sum(len(changes) for changes in categorized_changes.values())
            
            start_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
            end_date = datetime.utcnow().strftime('%Y-%m-%d')
            
            # Project header - using original style
            report.append(f"\n## Project: [{project_name}]({gerrit_url}/q/project:{project_name})\n")
            report.append(f"**Period:** {start_date} to {end_date} ({days} days)\n")
            report.append(f"**Changes:** {project_total}\n")
            report.append("\n")
        
            # Merged changes
            if categorized_changes['merged']:
                report.append(f"\n## ✅ Merged MRs ({len(categorized_changes['merged'])})\n")
                for change in categorized_changes['merged']:
                    report.append(f"\n### [{change['subject']}]({change['url']})\n")
                    report.append(f"- **Change #:** {change['number']}\n")
                    report.append(f"- **Author:** {change['owner']}\n")
                    report.append(f"- **Changes:** +{change['insertions']} / -{change['deletions']} lines\n")
                    report.append(f"- **Updated:** {change['updated']}\n")
            
            # Open changes
            if categorized_changes['open']:
                report.append(f"\n## 🔍 Open MRs ({len(categorized_changes['open'])})\n")
                for change in categorized_changes['open']:
                    report.append(f"\n### [{change['subject']}]({change['url']})\n")
                    report.append(f"- **Change #:** {change['number']}\n")
                    report.append(f"- **Author:** {change['owner']}\n")
                    report.append(f"- **Updated:** {change['updated']}\n")
            
            # Work in progress
            if categorized_changes['work_in_progress']:
                report.append(f"\n## 🚧 Work In Progress ({len(categorized_changes['work_in_progress'])})\n")
                for change in categorized_changes['work_in_progress']:
                    report.append(f"\n### [{change['subject']}]({change['url']})\n")
                    report.append(f"- **Change #:** {change['number']}\n")
                    report.append(f"- **Author:** {change['owner']}\n")
                    report.append(f"- **Updated:** {change['updated']}\n")
            
            # Abandoned changes
            if categorized_changes['abandoned']:
                report.append(f"\n## ❌ Abandoned MRs ({len(categorized_changes['abandoned'])})\n")
                for change in categorized_changes['abandoned']:
                    report.append(f"\n### [{change['subject']}]({change['url']})\n")
                    report.append(f"- **Change #:** {change['number']}\n")
                    report.append(f"- **Author:** {change['owner']}\n")
                    report.append(f"- **Updated:** {change['updated']}\n")
            
            report.append("\n---\n")
        
        # Footer
        report.append(f"\n*Report generated by Gerrit Activity Monitor*\n")
        report.append(f"*Gerrit Instance: {gerrit_url}*\n")
        
        return ''.join(report)
    
    def save_report(self, content: str, filename: str = "GERRIT_DAILY_REPORT.md") -> bool:
        """Save report to a file."""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            logger.info(f"Report saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False


class SlackNotifier:
    """Send notifications to Slack via webhook (optional)."""
    
    def __init__(self, webhook_url: str):
        """Initialize Slack notifier with webhook URL."""
        self.webhook_url = webhook_url
    def format_single_project_message(self, project_name: str, categorized_changes: Dict[str, List[Dict]], 
                                      days: int, project_index: int = 0, total_projects: int = 1) -> Dict:
        """Format a single project's changes into a Slack message."""
        project_total = sum(len(changes) for changes in categorized_changes.values())
        
        # Build message blocks for single project
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Daily Gerrit Activity Report",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Project:* `{project_name}`\n*Period:* Last {days} days\n*Changes:* {project_total}"
                }
            }
        ]
        
        # Add project counter if multiple projects
        if total_projects > 1:
            blocks.append({
                "type": "context",
                "elements": [{
                    "type": "mrkdwn",
                    "text": f"Project {project_index + 1} of {total_projects}"
                }]
            })
        
        blocks.append({
            "type": "divider"
        })
        
        # Add merged changes
        if categorized_changes['merged']:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*✅ Merged MRs ({len(categorized_changes['merged'])})*"
                }
            })
            
            for change in categorized_changes['merged'][:10]:
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
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🔍 Open MRs ({len(categorized_changes['open'])})*"
                }
            })
            
            for change in categorized_changes['open'][:10]:
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
        
        # Add work in progress
        if categorized_changes['work_in_progress']:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🚧 Work In Progress ({len(categorized_changes['work_in_progress'])})*"
                }
            })
            
            for change in categorized_changes['work_in_progress'][:5]:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                    }
                })
            
            if len(categorized_changes['work_in_progress']) > 5:
                blocks.append({
                    "type": "context",
                    "elements": [{
                        "type": "mrkdwn",
                        "text": f"_...and {len(categorized_changes['work_in_progress']) - 5} more WIP changes_"
                    }]
                })
        
        # Add abandoned changes
        if categorized_changes['abandoned']:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*❌ Abandoned MRs ({len(categorized_changes['abandoned'])})*"
                }
            })
            
            for change in categorized_changes['abandoned'][:5]:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                    }
                })
            
            if len(categorized_changes['abandoned']) > 5:
                blocks.append({
                    "type": "context",
                    "elements": [{
                        "type": "mrkdwn",
                        "text": f"_...and {len(categorized_changes['abandoned']) - 5} more abandoned changes_"
                    }]
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
    
    
    def format_message(self, all_categorized_changes: Dict[str, Dict[str, List[Dict]]],
                      projects_config: List[Dict]) -> Dict:
        """Format changes into a Slack message for multiple projects."""
        # Calculate total changes across all projects
        total_changes = 0
        for categorized in all_categorized_changes.values():
            total_changes += sum(len(changes) for changes in categorized.values())
        
        # Build message blocks
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Daily Gerrit Activity Report",
                    "emoji": True
                }
            }
        ]
        
        # Show different format based on number of projects
        if len(projects_config) > 1:
            # Multiple projects: show "Projects:" and "Total Changes:"
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Projects:* {', '.join([p['name'] for p in projects_config])}\n*Total Changes:* {total_changes}"
                }
            })
        else:
            # Single project: show "Project:" and "Changes:" (without "Total")
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Project:* {projects_config[0]['name']}\n*Changes:* {total_changes}"
                }
            })
        
        blocks.append({
            "type": "divider"
        })
        
        # Add section for each project (only for multiple projects)
        for project_config in projects_config:
            project_name = project_config['name']
            days = project_config.get('check_days', 7)
            
            if project_name not in all_categorized_changes:
                continue
            
            categorized_changes = all_categorized_changes[project_name]
            project_total = sum(len(changes) for changes in categorized_changes.values())
            project_display_name = project_name.split('/')[-1]
            
            # Project header (only show for multiple projects, since single project already shown above)
            if len(projects_config) > 1:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Project:* `{project_name}`\n*Period:* Last {days} days\n*Changes:* {project_total}"
                    }
                })
                blocks.append({
                    "type": "divider"
                })
        
            # Add merged changes for this project
            if categorized_changes['merged']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*✅ Merged MRs ({len(categorized_changes['merged'])})*"
                    }
                })
                
                # Slack has 50 block limit, so limit to 10 per category
                for change in categorized_changes['merged'][:10]:
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
            
            # Add open changes for this project
            if categorized_changes['open']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🔍 Open MRs ({len(categorized_changes['open'])})*"
                    }
                })
                
                for change in categorized_changes['open'][:10]:
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
            
            # Add work in progress changes for this project
            if categorized_changes['work_in_progress']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*🚧 Work In Progress ({len(categorized_changes['work_in_progress'])})*"
                    }
                })
                
                for change in categorized_changes['work_in_progress'][:5]:
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                        }
                    })
                
                if len(categorized_changes['work_in_progress']) > 5:
                    blocks.append({
                        "type": "context",
                        "elements": [{
                            "type": "mrkdwn",
                            "text": f"_...and {len(categorized_changes['work_in_progress']) - 5} more WIP changes_"
                        }]
                    })
            
            # Add abandoned changes for this project
            if categorized_changes['abandoned']:
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*❌ Abandoned MRs ({len(categorized_changes['abandoned'])})*"
                    }
                })
                
                for change in categorized_changes['abandoned'][:5]:
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"• <{change['url']}|#{change['number']}>: {change['subject']}\n  _by {change['owner']}_"
                        }
                    })
                
                if len(categorized_changes['abandoned']) > 5:
                    blocks.append({
                        "type": "context",
                        "elements": [{
                            "type": "mrkdwn",
                            "text": f"_...and {len(categorized_changes['abandoned']) - 5} more abandoned changes_"
                        }]
                    })
            
            # Add divider between projects (only for multiple projects)
            if len(projects_config) > 1:
                blocks.append({
                    "type": "divider"
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


class EmailNotifier:
    """Send email notifications via SMTP."""
    
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str,
                 smtp_password: str, from_email: str, to_emails: List[str]):
        """Initialize Email notifier with SMTP settings."""
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.to_emails = to_emails
    
    def send_email(self, subject: str, html_content: str, text_content: str) -> bool:
        """Send email with both HTML and plain text versions."""
        try:
            logger.info(f"Sending email to {', '.join(self.to_emails)}")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info("Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown report to clean HTML matching the reference design."""
        import re
        
        # Parse the markdown content
        lines = markdown_content.split('\n')
        
        # Extract key information
        total_changes = 0
        projects = []
        is_single_project = False
        
        for line in lines:
            if line.startswith('**Total Changes:**') or line.startswith('**Changes:**'):
                total_match = re.search(r'(\d+)', line)
                if total_match:
                    total_changes = int(total_match.group(1))
            elif line.startswith('**Projects:**'):
                # Multiple projects
                projects_match = re.search(r'\*\*Projects:\*\* (.+)', line)
                if projects_match:
                    projects = [p.strip() for p in projects_match.group(1).split(',')]
            elif line.startswith('**Project:**'):
                # Single project
                project_match = re.search(r'\*\*Project:\*\* (.+)', line)
                if project_match:
                    projects = [project_match.group(1)]
                    is_single_project = True
            elif line.startswith('## Project:'):
                # Extract project name from section header (fallback)
                project_match = re.search(r'\[([^\]]+)\]', line)
                if project_match and project_match.group(1) not in projects:
                    projects.append(project_match.group(1))
        
        # Build HTML sections
        html_parts = []
        
        # Format projects display
        if is_single_project or len(projects) == 1:
            # Single project format
            project_label = "Project"
            changes_label = "Changes"
            projects_str = projects[0] if projects else 'N/A'
        else:
            # Multiple projects format
            project_label = "Projects"
            changes_label = "Total Changes"
            projects_str = ', '.join(projects) if projects else 'N/A'
        
        html_parts.append(f'''
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #ffffff;">
            <div style="padding: 30px 20px 20px 20px; font-size: 14px; color: #333; line-height: 1.6;">
                <p style="margin: 0 0 5px 0;">Hi Team,</p>
                <p style="margin: 0;">Please find below the Gerrit activity report.</p>
            </div>
            
            <div style="background-color: #f5f5f5; padding: 30px 20px;">
                <div style="background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 1200px; margin: 0 auto;">
                <h1 style="margin: 0 0 20px 0; font-size: 24px; font-weight: 600; color: #1a1a1a; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">📊</span> Gerrit Activity Report
                </h1>
                
                <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0;">
                    <p style="margin: 5px 0; font-size: 14px; color: #333;">
                        <strong>{project_label}:</strong> {projects_str}
                    </p>
                    <p style="margin: 5px 0; font-size: 14px; color: #333;">
                        <strong>{changes_label}:</strong> {total_changes}
                    </p>
                </div>
        ''')
        
        # Parse sections
        current_section = None
        section_items = []
        current_project = None
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detect project headers
            if line.startswith('## Project:'):
                # Close previous project section if exists
                if current_section and section_items:
                    html_parts.append(self._render_section(current_section, section_items))
                    html_parts.append('</div>')
                    section_items = []
                    current_section = None
                
                # Extract project info
                project_match = re.search(r'\[([^\]]+)\]', line)
                if project_match:
                    current_project = project_match.group(1)
                    
                    # Get period and changes from next lines
                    period = ""
                    changes = ""
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith('**Period:**'):
                        period_match = re.search(r'(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) \((\d+) days\)', lines[i + 1])
                        if period_match:
                            period = f"Last {period_match.group(3)} days"
                    if i + 2 < len(lines) and lines[i + 2].strip().startswith('**Changes:**'):
                        changes_match = re.search(r'(\d+)', lines[i + 2])
                        if changes_match:
                            changes = changes_match.group(1)
                    
                    # Add project header (only for multiple projects, since single project already shown above)
                    if not is_single_project and len(projects) > 1:
                        html_parts.append(f'''
                        <div style="margin-top: 30px; padding-top: 20px;">
                            <h2 style="margin: 0 0 15px 0; font-size: 20px; font-weight: 600; color: #1a1a1a;">
                                Project: <span style="color: #d63384; font-family: monospace;">{current_project}</span>
                            </h2>
                            <p style="margin: 5px 0; font-size: 14px; color: #666;">
                                <strong>Period:</strong> {period} • <strong>Changes:</strong> {changes}
                            </p>
                        </div>
                        ''')
            
            # Detect section headers
            elif line.startswith('## ✅ Merged'):
                if current_section and section_items:
                    html_parts.append(self._render_section(current_section, section_items))
                current_section = 'merged'
                section_items = []
                count = re.search(r'\((\d+)\)', line)
                html_parts.append(f'''
                <div style="margin-top: 25px;">
                    <h2 style="margin: 0 0 15px 0; font-size: 18px; font-weight: 600; color: #1a1a1a; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">✅</span> Merged MRs ({count.group(1) if count else 0})
                    </h2>
                ''')
            elif line.startswith('## 🔍 Open'):
                if current_section and section_items:
                    html_parts.append(self._render_section(current_section, section_items))
                    html_parts.append('</div>')
                current_section = 'open'
                section_items = []
                count = re.search(r'\((\d+)\)', line)
                html_parts.append(f'''
                <div style="margin-top: 25px;">
                    <h2 style="margin: 0 0 15px 0; font-size: 18px; font-weight: 600; color: #1a1a1a; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">🔍</span> Open MRs ({count.group(1) if count else 0})
                    </h2>
                ''')
            elif line.startswith('## 🚧 Work In Progress'):
                if current_section and section_items:
                    html_parts.append(self._render_section(current_section, section_items))
                    html_parts.append('</div>')
                current_section = 'wip'
                section_items = []
                count = re.search(r'\((\d+)\)', line)
                html_parts.append(f'''
                <div style="margin-top: 25px;">
                    <h2 style="margin: 0 0 15px 0; font-size: 18px; font-weight: 600; color: #1a1a1a; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">🚧</span> Work In Progress ({count.group(1) if count else 0})
                    </h2>
                ''')
            elif line.startswith('## ❌ Abandoned'):
                if current_section and section_items:
                    html_parts.append(self._render_section(current_section, section_items))
                    html_parts.append('</div>')
                current_section = 'abandoned'
                section_items = []
                count = re.search(r'\((\d+)\)', line)
                html_parts.append(f'''
                <div style="margin-top: 25px;">
                    <h2 style="margin: 0 0 15px 0; font-size: 18px; font-weight: 600; color: #1a1a1a; display: flex; align-items: center;">
                        <span style="margin-right: 8px;">❌</span> Abandoned MRs ({count.group(1) if count else 0})
                    </h2>
                ''')
            elif line.startswith('### '):
                # Parse change item with ALL details
                title_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
                if title_match:
                    item = {
                        'title': title_match.group(1),
                        'url': title_match.group(2),
                        'details': []
                    }
                    
                    # Collect ALL detail lines
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith('- '):
                        detail = lines[j].strip()[2:]  # Remove "- " prefix
                        item['details'].append(detail)
                        j += 1
                    
                    section_items.append(item)
                    i = j - 1
            
            i += 1
        
        # Render last section
        if current_section and section_items:
            html_parts.append(self._render_section(current_section, section_items))
        
        html_parts.append('''
                </div>
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
                    <div style="font-size: 12px; color: #666; text-align: center;">
                        Generated on ''' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC') + '''
                    </div>
                </div>
                </div>
            </div>
            
            <div style="padding: 20px 20px 30px 20px; font-size: 14px; color: #333; line-height: 1.6;">
                <p style="margin: 0 0 5px 0;">Regards,</p>
                <p style="margin: 0;">Nikhil</p>
            </div>
        </div>
        ''')
        
        return ''.join(html_parts)
    
    def _render_section(self, section_type: str, items: List[Dict]) -> str:
        """Render a section of changes with all original details."""
        import re
        html = '<ul style="list-style: none; padding: 0; margin: 0;">'
        
        for item in items:
            # Extract change number from first detail if available
            change_num = ""
            for detail in item['details']:
                if 'Change #:' in detail:
                    num_match = re.search(r'(\d+)', detail)
                    if num_match:
                        change_num = num_match.group(1)
                        break
            
            html += f'''
            <li style="margin-bottom: 20px; padding-left: 0;">
                <div style="font-size: 16px; line-height: 1.6;">
                    <div style="margin-bottom: 8px;">
                        <span style="margin-right: 5px;">•</span>
                        <a href="{item['url']}" style="color: #0969da; text-decoration: none; font-weight: 500;">#{change_num}</a>:
                        {item['title']}
                    </div>
            '''
            
            # Add all detail lines
            if item['details']:
                html += '<div style="margin-left: 15px; font-size: 14px; color: #666;">'
                for detail in item['details']:
                    # Make the detail labels bold
                    detail_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', detail)
                    html += f'<div style="margin: 2px 0;">{detail_html}</div>'
                html += '</div>'
            
            html += '''
                </div>
            </li>
            '''
        
        html += '</ul>'
        return html


def main():
    """Main execution function."""
    # Load environment variables
    load_dotenv()
    
    # Get Slack webhook URL from environment (optional)
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    
    # Initialize monitor
    monitor = GerritMonitor()
    
    # Log projects being monitored
    logger.info(f"Monitoring {len(monitor.projects)} project(s):")
    for project_config in monitor.projects:
        project_name = project_config['name']
        check_days = project_config.get('check_days', 7)
        logger.info(f"  - {project_name} (last {check_days} days)")
    
    # Fetch changes for all projects
    all_changes = monitor.fetch_all_changes()
    
    # Categorize changes for each project
    all_categorized = {}
    for project_name, changes in all_changes.items():
        categorized = monitor.categorize_changes(changes)
        all_categorized[project_name] = categorized
        
        project_total = sum(len(c) for c in categorized.values())
        logger.info(f"Project {project_name}: {project_total} changes found")
    
    # Generate markdown report
    report_generator = ReportGenerator()
    markdown_report = report_generator.generate_markdown_report(
        all_categorized,
        monitor.projects,
        monitor.gerrit_url
    )
    
    # Save report to file
    report_saved = report_generator.save_report(markdown_report)
    
    if report_saved:
        logger.info("✅ Multi-project report generated successfully!")
        logger.info("📄 Report saved to: GERRIT_DAILY_REPORT.md")
    else:
        logger.error("❌ Failed to generate report")
        sys.exit(1)
    
    # Optionally send to Slack if webhook URL is provided
    if slack_webhook_url:
        logger.info("Slack webhook URL found, sending notifications...")
        notifier = SlackNotifier(slack_webhook_url)
        
        # Send separate message for each project to avoid size limits
        total_projects = len(monitor.projects)
        slack_success_count = 0
        slack_fail_count = 0
        
        for idx, project_config in enumerate(monitor.projects):
            project_name = project_config['name']
            days = project_config.get('check_days', 7)
            
            if project_name in all_categorized:
                logger.info(f"Sending Slack notification for {project_name} ({idx + 1}/{total_projects})...")
                message = notifier.format_single_project_message(
                    project_name,
                    all_categorized[project_name],
                    days,
                    idx,
                    total_projects
                )
                
                if notifier.send_message(message):
                    slack_success_count += 1
                else:
                    slack_fail_count += 1
        
        if slack_success_count == total_projects:
            logger.info(f"✅ All {total_projects} Slack notifications sent successfully!")
        elif slack_success_count > 0:
            logger.warning(f"⚠️  Sent {slack_success_count}/{total_projects} Slack notifications ({slack_fail_count} failed)")
        else:
            logger.warning("⚠️  Failed to send Slack notifications (report still saved)")
    else:
        logger.info("ℹ️  No Slack webhook URL provided, skipping Slack notification")
        logger.info("   To enable Slack notifications, set SLACK_WEBHOOK_URL in .env file")
    
    # Optionally send email if SMTP settings are provided
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT', '587')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    to_emails_str = os.getenv('TO_EMAILS')
    
    if all([smtp_host, smtp_user, smtp_password, from_email, to_emails_str]):
        logger.info("Email settings found, sending email notification...")
        # Type assertions - all values are guaranteed to be non-None by the all() check above
        assert smtp_host is not None
        assert smtp_user is not None
        assert smtp_password is not None
        assert from_email is not None
        assert to_emails_str is not None
        
        to_emails = [email.strip() for email in to_emails_str.split(',')]
        
        email_notifier = EmailNotifier(
            smtp_host=smtp_host,
            smtp_port=int(smtp_port),
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            from_email=from_email,
            to_emails=to_emails
        )
        
        # Generate email subject
        report_date = datetime.utcnow().strftime('%Y-%m-%d')
        project_names = ', '.join([p['name'].split('/')[-1] for p in monitor.projects])
        subject = f"📊 Gerrit Activity Report - {project_names} - {report_date}"
        
        # Convert markdown to HTML
        html_content = email_notifier.markdown_to_html(markdown_report)
        
        email_success = email_notifier.send_email(
            subject=subject,
            html_content=html_content,
            text_content=markdown_report
        )
        
        if email_success:
            logger.info("✅ Email notification sent successfully!")
        else:
            logger.warning("⚠️  Failed to send email notification (report still saved)")
    else:
        logger.info("ℹ️  Email settings not fully configured, skipping email notification")
        logger.info("   To enable email notifications, set SMTP_HOST, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL, and TO_EMAILS in .env file")


if __name__ == "__main__":
    main()

