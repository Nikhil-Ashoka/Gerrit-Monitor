# Quick Start Guide

Get your Gerrit monitor up and running in 3 minutes!

## 🚀 Fastest Setup (GitHub Actions - Recommended)

### Step 1: Deploy to GitHub (2 minutes)

1. **Fork or clone this repository to your GitHub account**

2. **Enable GitHub Actions:**
   - Go to **Actions** tab
   - Click **"I understand my workflows, go ahead and enable them"**

3. **Test it now (optional):**
   - Go to **Actions** → **Daily Gerrit Monitor**
   - Click **Run workflow** → **Run workflow**
   - Wait ~30 seconds and check the workflow output!

### Done! 🎉

Your monitor will now run automatically **every day at 7:05 AM UTC** (12:35 PM IST) and generate a detailed report file.

---

## 📧 Optional: Add Slack Notifications (2 extra minutes)

If you want to receive Slack notifications in addition to the generated report:

### Step 1: Get Your Slack Webhook

1. Go to https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name it "Gerrit Monitor" and select your workspace
3. Click **Incoming Webhooks** → Toggle ON
4. Click **Add New Webhook to Workspace** → Select your channel → **Allow**
5. **Copy the webhook URL** (looks like `https://hooks.slack.com/services/...`)

### Step 2: Add Webhook to GitHub

1. Go to your repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `SLACK_WEBHOOK_URL`
4. Value: Paste your webhook URL
5. Click **Add secret**

Now you'll get both the report file AND Slack notifications!

---

## 💻 Local Setup (Alternative)

If you prefer to run locally:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run

```bash
python monitor.py
```

This will generate `GERRIT_DAILY_REPORT.md` in the current directory!

### Step 3: (Optional) Add Slack

```bash
cp .env.example .env
# Edit .env and add your SLACK_WEBHOOK_URL
python monitor.py
```

Now you'll get both the report file AND Slack notification!

---

## 📝 What You'll Get

Every day, a detailed markdown report (`GERRIT_DAILY_REPORT.md`) with:

- 📊 **Report metadata** - Date, project, period covered
- ✅ **Merged changes** - What got merged this week (with +/- line counts)
- 🔍 **Open changes** - What needs review
- 🚧 **Work in progress** - What's being worked on
- ❌ **Abandoned changes** - What was dropped

Each change includes:
- Direct link to Gerrit
- Change number and subject
- Author name
- Last updated timestamp
- Code statistics (for merged changes)

**Plus:** If Slack is configured, you'll also get a formatted Slack message!

---

## ⚙️ Customization

Edit `config.json` to change:

```json
{
  "gerrit_url": "https://gerrit.openbmc.org",
  "project": "openbmc/webui-vue",
  "check_days": 7,
  "max_results": 100
}
```

- `check_days`: Change to 14 for bi-daily reports
- `project`: Monitor a different project
- `max_results`: Increase if you have many changes

---

## 🔧 Troubleshooting

**No report file generated?**
- Check the Actions logs for errors
- Verify the Gerrit URL and project name in config.json
- Ensure GitHub Actions is enabled

**Empty report?**
- Normal if there's no activity in the period
- Try increasing `check_days` in config.json

**Slack not working?**
- Slack is optional - the report file is generated regardless
- Check your webhook URL is correct
- Verify the secret is set in GitHub (for Actions)

**Need help?**
See [SETUP.md](SETUP.md) for detailed instructions.

---

## 📅 Schedule

Default schedule: **Every day at 7:05 AM UTC (12:35 PM IST)**

To change the schedule, edit `.github/workflows/daily-monitor.yml`:

```yaml
schedule:
  - cron: '5 7 * * *'  # Minute Hour Day Month Weekday
```

Examples:
- `5 7 * * *` - Every day at 7:05 AM UTC (12:35 PM IST)
- `5 7 * * 1` - Every Monday at 7:05 AM UTC (12:35 PM IST)
- `5 7 * * 1,5` - Every Monday and Friday at 7:05 AM UTC (12:35 PM IST)
- `5 7 1 * *` - First day of every month at 7:05 AM UTC (12:35 PM IST)

---

## 🎯 Next Steps

1. ✅ Wait for your first daily report (runs at 12:35 PM IST)
2. ✅ Customize the report period in config.json (default: 7 days)
3. ✅ Adjust the schedule if needed (edit `.github/workflows/daily-monitor.yml`)
4. ✅ Consider monitoring additional projects or repositories

Happy monitoring! 🚀