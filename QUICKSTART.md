# Quick Start Guide

Get your Gerrit monitor up and running in 5 minutes!

## 🚀 Fastest Setup (GitHub Actions - Recommended)

### Step 1: Get Your Slack Webhook (2 minutes)

1. Go to https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name it "Gerrit Monitor" and select your workspace
3. Click **Incoming Webhooks** → Toggle ON
4. Click **Add New Webhook to Workspace** → Select your channel → **Allow**
5. **Copy the webhook URL** (looks like `https://hooks.slack.com/services/...`)

### Step 2: Deploy to GitHub (3 minutes)

1. **Fork or clone this repository to your GitHub account**

2. **Add your Slack webhook as a secret:**
   - Go to your repo → **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `SLACK_WEBHOOK_URL`
   - Value: Paste your webhook URL
   - Click **Add secret**

3. **Enable GitHub Actions:**
   - Go to **Actions** tab
   - Click **"I understand my workflows, go ahead and enable them"**

4. **Test it now (optional):**
   - Go to **Actions** → **Weekly Gerrit Monitor**
   - Click **Run workflow** → **Run workflow**
   - Wait ~30 seconds and check your Slack channel!

### Done! 🎉

Your monitor will now run automatically **every Monday at 9:00 AM UTC** (2:30 PM IST).

---

## 💻 Local Setup (Alternative)

If you prefer to run locally:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure

```bash
cp .env.example .env
# Edit .env and add your SLACK_WEBHOOK_URL
```

### Step 3: Run

```bash
python monitor.py
```

Check your Slack channel for the report!

---

## 📝 What You'll Get

Every week, you'll receive a Slack message with:

- ✅ **Merged changes** - What got merged this week
- 🔍 **Open changes** - What needs review
- 🚧 **Work in progress** - What's being worked on
- ❌ **Abandoned changes** - What was dropped

Each change includes:
- Direct link to Gerrit
- Change number and subject
- Author name
- Lines added/removed (for merged changes)

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

- `check_days`: Change to 14 for bi-weekly reports
- `project`: Monitor a different project
- `max_results`: Increase if you have many changes

---

## 🔧 Troubleshooting

**No message in Slack?**
- Check your webhook URL is correct
- Verify the secret is set in GitHub (for Actions)
- Check the Actions logs for errors

**Empty report?**
- Normal if there's no activity in the period
- Try increasing `check_days` in config.json

**Need help?**
See [SETUP.md](SETUP.md) for detailed instructions.

---

## 📅 Schedule

Default schedule: **Every Monday at 9:00 AM UTC**

To change the schedule, edit `.github/workflows/weekly-monitor.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Minute Hour Day Month Weekday
```

Examples:
- `0 9 * * 1` - Every Monday at 9 AM
- `0 9 * * 5` - Every Friday at 9 AM  
- `0 9 1 * *` - First day of every month at 9 AM
- `0 9 * * 1,5` - Every Monday and Friday at 9 AM

---

## 🎯 Next Steps

1. ✅ Wait for your first weekly report
2. ✅ Customize the schedule if needed
3. ✅ Share with your team
4. ✅ Monitor additional projects (see SETUP.md)

Happy monitoring! 🚀