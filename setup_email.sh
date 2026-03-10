#!/bin/bash
# Quick setup script for email configuration

echo "================================================"
echo "📧 Gerrit Monitor - Email Setup"
echo "================================================"
echo ""
echo "This script will help you configure email notifications."
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✅ .env file found"
else
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
fi

echo ""
echo "📋 Next steps:"
echo ""
echo "1. Edit the .env file with your email settings:"
echo "   - SMTP_HOST (e.g., smtp.gmail.com)"
echo "   - SMTP_PORT (usually 587)"
echo "   - SMTP_USER (your email address)"
echo "   - SMTP_PASSWORD (your app password)"
echo "   - FROM_EMAIL (your email address)"
echo "   - TO_EMAILS (already set to a.nikhil@ibm.com)"
echo ""
echo "2. For Gmail users:"
echo "   - Enable 2-Step Verification"
echo "   - Generate an App Password at:"
echo "     https://myaccount.google.com/apppasswords"
echo ""
echo "3. Test your configuration:"
echo "   python test_email.py"
echo ""
echo "📖 For detailed instructions, see EMAIL_SETUP.md"
echo ""
echo "================================================"

# Made with Bob
