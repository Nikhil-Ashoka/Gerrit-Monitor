# Setup Guide - Gerrit Daily Activity Monitor

This guide will walk you through setting up the Gerrit Daily Activity Monitor to automatically track and report repository activities to Slack.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Slack Webhook Setup](#slack-webhook-setup)
3. [Local Setup](#local-setup)
4. [GitHub Actions Setup (Recommended)](#github-actions-setup-recommended)
5. [Alternative: Local Cron Setup](#alternative-local-cron-setup)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- A Slack workspace where you can create webhooks
- (Optional) A GitHub account for automated execution

## Slack Webhook Setup

1. **Create a Slack App:**
   - Go to https://api.slack.com/apps
   - Click "Create New App"
   - Choose "From scratch"
   - Name your app (e.g., "Gerrit Monitor")
   - Select your workspace

2. **Enable Incoming Webhooks:**
   - In your app settings, click "Incoming Webhooks"
   - Toggle "Activate Incoming Webhooks" to ON
   - Click "Add New Webhook to Workspace"
   - Select the channel where you want to receive updates
   - Click "Allow"

3. **Copy the Webhook URL:**
   - You'll see a webhook URL like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX`
   - Copy this URL - you'll need it in the next steps

## Local Setup

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd gerrit-monitor
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Slack webhook URL:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 4. (Optional) Customize Configuration

Edit `config.json` to customize:

```json
{
  "gerrit_url": "https://gerrit.openbmc.org",
  "project": "openbmc/webui-vue",
  "check_days": 7,
  "max_results": 100
}
```

- `gerrit_url`: The Gerrit instance URL
- `project`: The project path to monitor
- `check_days`: Number of days to look back (default: 7)
- `max_results`: Maximum number of changes to fetch (default: 100)

### 5. Test the Setup

Run the monitor manually to verify everything works:

```bash
python monitor.py
```

You should see:
- Log messages indicating the script is running
- A message posted to your Slack channel with the daily report

## GitHub Actions Setup (Recommended)

This is the **easiest way** to run the monitor automatically without any server or local machine dependencies.

### 1. Fork or Push to GitHub

Push your local repository to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Add Slack Webhook as GitHub Secret

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SLACK_WEBHOOK_URL`
5. Value: Your Slack webhook URL
6. Click **Add secret**

### 3. Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. If prompted, click **"I understand my workflows, go ahead and enable them"**
3. The workflow is already configured in `.github/workflows/daily-monitor.yml`

### 4. Verify the Schedule

The workflow is set to run:
- **Every Monday at 9:00 AM UTC** (2:30 PM IST)
- You can also trigger it manually from the Actions tab

### 5. Manual Trigger (Optional)

To test immediately:
1. Go to **Actions** tab
2. Click **Daily Gerrit Monitor** workflow
3. Click **Run workflow** → **Run workflow**

## Alternative: Local Cron Setup

If you prefer to run the monitor on your local machine or server:

### On Linux/macOS:

1. Make the script executable:
```bash
chmod +x monitor.py
```

2. Edit your crontab:
```bash
crontab -e
```

3. Add this line to run every Monday at 9 AM:
```
0 9 * * 1 cd /path/to/gerrit-monitor && /usr/bin/python3 monitor.py >> /path/to/gerrit-monitor/monitor.log 2>&1
```

Replace `/path/to/gerrit-monitor` with your actual path.

### On Windows:

1. Open **Task Scheduler**
2. Create a new task:
   - **Trigger**: Daily, every day at 9:00 AM
   - **Action**: Start a program
   - **Program**: `python`
   - **Arguments**: `C:\path\to\gerrit-monitor\monitor.py`
   - **Start in**: `C:\path\to\gerrit-monitor`

## Testing

### Test the Gerrit API Connection

```bash
python -c "from monitor import GerritMonitor; m = GerritMonitor(); print(f'Found {len(m.fetch_changes())} changes')"
```

### Test the Slack Integration

```bash
python monitor.py
```

Check your Slack channel for the report.

### Test with Different Time Periods

Temporarily modify `config.json` to check different periods:

```json
{
  "check_days": 14
}
```

## Troubleshooting

### Issue: "SLACK_WEBHOOK_URL environment variable not set"

**Solution:** Make sure you've created the `.env` file with your webhook URL.

### Issue: "No changes found or error fetching changes"

**Possible causes:**
1. The Gerrit API might be temporarily unavailable
2. The project name might be incorrect
3. There might be no activity in the specified period

**Solution:** 
- Verify the project name in `config.json`
- Try increasing `check_days` to see more history
- Check if you can access the Gerrit URL in your browser

### Issue: "Error sending message to Slack"

**Possible causes:**
1. Invalid webhook URL
2. Network connectivity issues
3. Slack webhook has been revoked

**Solution:**
- Verify your webhook URL is correct
- Test the webhook with curl:
```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_WEBHOOK_URL
```

### Issue: GitHub Actions workflow not running

**Possible causes:**
1. Workflow is disabled
2. Repository is private and you've exceeded free minutes
3. Secret is not set correctly

**Solution:**
- Check the Actions tab for any errors
- Verify the `SLACK_WEBHOOK_URL` secret is set
- Try triggering manually first

### Issue: Empty or incomplete reports

**Solution:**
- Check the logs for any errors
- Verify the `max_results` setting isn't too low
- Ensure the date range covers the period you're interested in

## Advanced Configuration

### Monitoring Multiple Projects

To monitor multiple projects, you can:

1. Create separate configuration files:
```bash
cp config.json config-project1.json
cp config.json config-project2.json
```

2. Modify each config file with different projects

3. Run the monitor with different configs:
```bash
python monitor.py  # Uses config.json by default
```

Or modify the script to accept a config file parameter.

### Custom Message Formatting

Edit the `format_message` method in `monitor.py` to customize the Slack message format.

### Filtering Changes

Modify the `categorize_changes` method to add custom filters based on:
- Author
- File paths
- Commit message patterns
- Review status

## Support

For issues or questions:
1. Check the logs in `monitor.log` (if configured)
2. Review the troubleshooting section above
3. Check the GitHub Actions logs if using automated execution
4. Verify your Gerrit API access and Slack webhook

## Next Steps

Once everything is working:
1. ✅ Verify the first daily report arrives successfully
2. ✅ Adjust the schedule if needed (edit `.github/workflows/daily-monitor.yml`)
3. ✅ Customize the message format to your team's preferences
4. ✅ Consider monitoring additional projects or repositories