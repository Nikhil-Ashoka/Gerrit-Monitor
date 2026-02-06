#!/usr/bin/env python3
"""
Test script to verify Gerrit Monitor setup
"""

import os
import sys
import json
from dotenv import load_dotenv

def test_environment():
    """Test environment variables."""
    print("🔍 Testing Environment Variables...")
    load_dotenv()
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not found in environment")
        print("   Please create a .env file with your webhook URL")
        return False
    
    if not webhook_url.startswith('https://hooks.slack.com/'):
        print("⚠️  Warning: Webhook URL doesn't look like a Slack webhook")
        print(f"   Got: {webhook_url[:50]}...")
    else:
        print("✅ SLACK_WEBHOOK_URL is set")
    
    return True

def test_config():
    """Test configuration file."""
    print("\n🔍 Testing Configuration File...")
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['gerrit_url', 'project', 'check_days']
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            print(f"❌ Missing required config keys: {missing_keys}")
            return False
        
        print("✅ config.json is valid")
        print(f"   Gerrit URL: {config['gerrit_url']}")
        print(f"   Project: {config['project']}")
        print(f"   Check Days: {config['check_days']}")
        return True
        
    except FileNotFoundError:
        print("❌ config.json not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return False

def test_dependencies():
    """Test Python dependencies."""
    print("\n🔍 Testing Python Dependencies...")
    
    try:
        import requests
        print("✅ requests library installed")
    except ImportError:
        print("❌ requests library not installed")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv library installed")
    except ImportError:
        print("❌ python-dotenv library not installed")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def test_gerrit_connection():
    """Test connection to Gerrit API."""
    print("\n🔍 Testing Gerrit API Connection...")
    
    try:
        import requests
        from monitor import GerritMonitor
        
        monitor = GerritMonitor()
        print(f"   Connecting to: {monitor.gerrit_url}")
        print(f"   Project: {monitor.project}")
        
        # Try to fetch changes
        changes = monitor.fetch_changes()
        
        if changes is None:
            print("❌ Failed to fetch changes from Gerrit")
            return False
        
        print(f"✅ Successfully connected to Gerrit")
        print(f"   Found {len(changes)} changes in the last {monitor.check_days} days")
        
        if len(changes) > 0:
            print(f"   Latest change: {changes[0].get('subject', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Gerrit: {e}")
        return False

def test_slack_webhook():
    """Test Slack webhook."""
    print("\n🔍 Testing Slack Webhook...")
    
    try:
        import requests
        load_dotenv()
        
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if not webhook_url:
            print("❌ SLACK_WEBHOOK_URL not set")
            return False
        
        # Send a test message
        test_message = {
            "text": "🧪 Test message from Gerrit Monitor setup script"
        }
        
        print("   Sending test message to Slack...")
        response = requests.post(
            webhook_url,
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Successfully sent test message to Slack")
            print("   Check your Slack channel for the test message!")
            return True
        else:
            print(f"❌ Failed to send message. Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Slack webhook: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Gerrit Monitor - Setup Test")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Environment", test_environment),
        ("Configuration", test_config),
        ("Gerrit Connection", test_gerrit_connection),
        ("Slack Webhook", test_slack_webhook),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name} test: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run 'python monitor.py' to generate a full report")
        print("2. Set up GitHub Actions for automated weekly runs")
        print("3. See QUICKSTART.md for more information")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("See SETUP.md for detailed setup instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
