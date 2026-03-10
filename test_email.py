#!/usr/bin/env python3
"""
Test script to send a Gerrit report email immediately.
This is useful for testing email configuration before setting up the weekly schedule.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from monitor.py
from monitor import GerritMonitor, ReportGenerator, EmailNotifier
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Test email sending functionality."""
    
    # Check if email settings are configured
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT', '587')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    to_emails_str = os.getenv('TO_EMAILS')
    
    if not all([smtp_host, smtp_user, smtp_password, from_email, to_emails_str]):
        logger.error("❌ Email settings not fully configured!")
        logger.error("Please set the following environment variables in your .env file:")
        logger.error("  - SMTP_HOST")
        logger.error("  - SMTP_PORT (optional, defaults to 587)")
        logger.error("  - SMTP_USER")
        logger.error("  - SMTP_PASSWORD")
        logger.error("  - FROM_EMAIL")
        logger.error("  - TO_EMAILS")
        sys.exit(1)
    
    logger.info("✅ Email settings found")
    logger.info(f"SMTP Host: {smtp_host}")
    logger.info(f"SMTP Port: {smtp_port}")
    logger.info(f"From: {from_email}")
    logger.info(f"To: {to_emails_str}")
    
    # Initialize monitor
    monitor = GerritMonitor()
    
    # Override check_days for weekly report
    monitor.check_days = 7
    
    logger.info(f"Monitoring project: {monitor.project}")
    logger.info(f"Checking last {monitor.check_days} days")
    
    # Fetch changes
    logger.info("Fetching changes from Gerrit...")
    changes = monitor.fetch_changes()
    
    # Categorize changes
    categorized = monitor.categorize_changes(changes)
    
    # Generate markdown report
    report_generator = ReportGenerator()
    markdown_report = report_generator.generate_markdown_report(
        categorized, 
        monitor.project, 
        monitor.check_days,
        monitor.gerrit_url
    )
    
    # Save report to file
    report_saved = report_generator.save_report(markdown_report)
    
    if report_saved:
        logger.info("✅ Report generated successfully!")
        logger.info("📄 Report saved to: GERRIT_DAILY_REPORT.md")
    else:
        logger.error("❌ Failed to generate report")
        sys.exit(1)
    
    # Send email
    logger.info("\n" + "="*60)
    logger.info("Sending test email...")
    logger.info("="*60 + "\n")
    
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
    from datetime import datetime
    report_date = datetime.utcnow().strftime('%Y-%m-%d')
    subject = f"📊 [TEST] Gerrit Weekly Activity Report - {monitor.project} - {report_date}"
    
    # Convert markdown to HTML
    html_content = email_notifier.markdown_to_html(markdown_report)
    
    email_success = email_notifier.send_email(
        subject=subject,
        html_content=html_content,
        text_content=markdown_report
    )
    
    if email_success:
        logger.info("\n" + "="*60)
        logger.info("✅ TEST EMAIL SENT SUCCESSFULLY!")
        logger.info("="*60)
        logger.info(f"Check your inbox at: {to_emails_str}")
        logger.info("If you don't see it, check your spam folder.")
    else:
        logger.error("\n" + "="*60)
        logger.error("❌ FAILED TO SEND TEST EMAIL")
        logger.error("="*60)
        logger.error("Please check your SMTP settings and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
