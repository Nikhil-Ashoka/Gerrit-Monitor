# Gerrit Monitor

Automated monitoring for Gerrit projects with support for markdown report generation, daily Slack notifications, and weekly email delivery through GitHub Actions or local execution.

## Overview

This repository provides an automated solution for monitoring Gerrit projects, collecting recent Gerrit activity, generating a markdown report, and distributing the results through Slack (daily) or email (weekly).

The current configuration monitors [`openbmc/webui-vue`](https://gerrit.openbmc.org/q/project:openbmc/webui-vue). The monitor can be configured to work with any Gerrit projects by updating [`config.json`](config.json).

### What it does

- Monitors configurable Gerrit projects
- Fetches changes from a configurable time window
- Categorizes results by status such as merged, open, work in progress, and abandoned
- Generates a markdown activity report in the repository root
- Posts daily formatted notifications to Slack
- Sends weekly email reports
- Supports both GitHub Actions automation and local/manual execution

### Why use it

- No dedicated server required when using GitHub Actions
- Simple configuration through [`config.json`](config.json) and environment variables
- Easy to customize schedules, monitored project, reporting period, and notification behavior
- Includes workflow automation and optional notification support

## Features

- Daily Gerrit activity monitoring with Slack notifications
- Weekly Gerrit activity monitoring with email reports
- Markdown report generation in [`GERRIT_DAILY_REPORT.md`](GERRIT_DAILY_REPORT.md)
- Slack webhook notifications (daily workflow only)
- Weekly HTML email reporting (weekly workflow only)
- GitHub Actions workflows for automated execution
- Local cron or manual execution support
- Troubleshooting guidance included in the repository documentation

## Project Structure

```text
gerrit-monitor/
├── monitor.py
├── config.json
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── GERRIT_DAILY_REPORT.md
└── .github/workflows/
    ├── daily-monitor.yml
    └── weekly-monitor.yml
```

### Core components

1. **Monitor application** — [`monitor.py`](monitor.py)
   - Connects to the Gerrit REST API
   - Fetches and categorizes changes
   - Generates the markdown report
   - Triggers optional Slack and email notifications

2. **Configuration** — [`config.json`](config.json), [`.env.example`](.env.example)
   - Stores Gerrit target settings
   - Controls lookback period and result limits
   - Documents optional notification environment variables

3. **Automation** — [`.github/workflows/daily-monitor.yml`](.github/workflows/daily-monitor.yml), [`.github/workflows/weekly-monitor.yml`](.github/workflows/weekly-monitor.yml)
   - Schedules automatic report generation
   - Uses GitHub Secrets for sensitive values
   - Supports manual workflow execution

4. **Report output** — [`GERRIT_DAILY_REPORT.md`](GERRIT_DAILY_REPORT.md)
   - Stores the generated markdown activity summary
   - Can be committed by workflows and uploaded as an artifact

## Architecture and Data Flow

```text
GitHub Actions or Local Scheduler
              │
              ▼
         monitor.py
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 Gerrit API  Report   Notifications
             File     (Slack / Email)
```

## Prerequisites

- Python 3.8 or higher
- Internet access to the Gerrit instance you want to monitor
- Optional: Slack workspace with webhook access
- Optional: GitHub repository for automated execution
- Optional: SMTP credentials for email delivery

## Installation

### Clone the repository

```bash
git clone <your-repo-url>
cd gerrit-monitor
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Optional virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, use `venv\Scripts\activate` instead of `source venv/bin/activate`.

## Quick Start

### Fastest path: GitHub Actions

1. Push or fork the repository to GitHub.
2. Enable GitHub Actions in the repository.
3. Optionally trigger the daily workflow manually from the Actions tab.
4. Review the generated report file after the workflow completes.

Default automation runs:
- **Daily workflow**: Every day at **9:00 AM UTC (2:30 PM IST)** - Sends to Slack only
- **Weekly workflow**: Every Monday at **9:00 AM UTC (2:30 PM IST)** - Sends to Email only

### Local quick start

```bash
pip install -r requirements.txt
python monitor.py
```

This generates [`GERRIT_DAILY_REPORT.md`](GERRIT_DAILY_REPORT.md) in the repository root.

## Configuration

Edit [`config.json`](config.json) to customize the monitored Gerrit projects and reporting window.

Example (Multi-Project Configuration):

```json
{
  "gerrit_url": "https://gerrit.openbmc.org",
  "projects": [
    {
      "name": "openbmc/webui-vue",
      "check_days": 2,
      "max_results": 100
    },
    {
      "name": "openbmc/bmcweb",
      "check_days": 2,
      "max_results": 100
    }
  ]
}
```

### Configuration fields

- `gerrit_url`: Gerrit instance URL
- `projects`: Array of project configurations, each containing:
  - `name`: Gerrit project path to monitor
  - `check_days`: Number of days to look back for this project
  - `max_results`: Maximum number of changes to fetch for this project

### Backward Compatibility

The monitor still supports the old single-project configuration format for backward compatibility:

```json
{
  "gerrit_url": "https://gerrit.openbmc.org",
  "project": "openbmc/webui-vue",
  "check_days": 7,
  "max_results": 100
}
```

## Usage

### Manual execution

Run the monitor directly:

```bash
python monitor.py
```

### Local cron execution

On Linux or macOS:

1. Make the script executable if desired:

```bash
chmod +x monitor.py
```

2. Open your crontab:

```bash
crontab -e
```

3. Add a schedule entry. Examples:

Daily at 7:05 AM UTC:

```text
5 7 * * * cd /path/to/gerrit-monitor && python monitor.py
```

Weekly on Monday at 9:00 AM UTC:

```text
0 9 * * 1 cd /path/to/gerrit-monitor && /usr/bin/python3 monitor.py >> /path/to/gerrit-monitor/monitor.log 2>&1
```

Replace `/path/to/gerrit-monitor` with your real path.

### Windows scheduled execution

Use Task Scheduler and configure:

- Trigger: Your preferred time or recurrence
- Program: `python`
- Arguments: Full path to [`monitor.py`](monitor.py)
- Start in: Repository directory

## GitHub Actions Setup

GitHub Actions is the recommended deployment model because it removes the need for a long-running local machine.

### Enable workflows

1. Push the repository to GitHub.
2. Open the **Actions** tab.
3. Enable workflows if GitHub prompts for approval.
4. Use the included workflows:
   - [`.github/workflows/daily-monitor.yml`](.github/workflows/daily-monitor.yml)
   - [`.github/workflows/weekly-monitor.yml`](.github/workflows/weekly-monitor.yml)

### Daily workflow behavior

The daily workflow runs automatically every day at **9:00 AM UTC (2:30 PM IST)** and:
- Generates the markdown report file
- Sends notifications to **Slack only** (no email)
- Requires `SLACK_WEBHOOK_URL` secret to be configured

### Weekly workflow behavior

The weekly workflow runs every **Monday at 9:00 AM UTC (2:30 PM IST)** and:
- Generates the markdown report file for the past 7 days
- Sends notifications to **Email only** (no Slack)
- Requires email-related secrets to be configured (SMTP_HOST, SMTP_USER, etc.)

### Manual workflow trigger

You can manually test either workflow from the GitHub Actions UI by selecting the workflow and choosing **Run workflow**.

## Slack Notification Setup

Slack integration is used for **daily reports only**.

### Create a Slack webhook

1. Go to <https://api.slack.com/apps>.
2. Create a new app from scratch.
3. Enable **Incoming Webhooks**.
4. Add a webhook to the target channel.
5. Copy the webhook URL.

### Local Slack configuration

Copy [`.env.example`](.env.example) to a local `.env` file and add:

```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### GitHub Actions Slack configuration

Add a repository secret:

- `SLACK_WEBHOOK_URL`

Path in GitHub:
**Settings → Secrets and variables → Actions**

## Email Notification Setup

Email support is used for **weekly reports only**.

The email values below are examples only and should be replaced with your own sender and recipient settings.

### Local email configuration

Set the relevant values in your local `.env` file:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
TO_EMAILS=team@example.com
```

### Gmail app password notes

1. Go to <https://myaccount.google.com/apppasswords>.
2. Enable 2-Step Verification if needed.
3. Create an app password for Mail.
4. Use the generated app password for `SMTP_PASSWORD`.

### GitHub Secrets for email automation

For weekly email automation, add these repository secrets:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `FROM_EMAIL`
- `TO_EMAILS`

Recommended values documented by the existing setup materials:

- `SMTP_HOST`: `smtp.gmail.com`
- `SMTP_PORT`: `587`

### Security considerations

- Do not commit your local `.env` file
- Keep credentials only in local environment files or GitHub Secrets
- GitHub Actions secrets remain masked in workflow logs

## Testing

### Test Gerrit API access quickly

```bash
python -c "from monitor import GerritMonitor; m = GerritMonitor(); print(f'Found {len(m.fetch_changes())} changes')"
```

### Test a normal monitor run

```bash
python monitor.py
```

Expected outputs may include:

- Report generation log messages
- A saved [`GERRIT_DAILY_REPORT.md`](GERRIT_DAILY_REPORT.md) file
- Optional Slack notification
- Optional email delivery, depending on configuration

## Output

The generated markdown report includes items such as:

- Report metadata
- Total change count
- Merged changes with code statistics where available
- Open changes awaiting review
- Work in progress changes
- Abandoned changes
- Direct links to Gerrit changes

If Slack is configured, a formatted Slack notification is also sent.
If email is configured, a formatted HTML email can also be delivered.

## Customization

### Add or remove monitored projects

Edit [`config.json`](config.json) to add, remove, or modify the projects you want to monitor.

Example - Adding a third project:

```json
{
  "gerrit_url": "https://gerrit.openbmc.org",
  "projects": [
    {
      "name": "openbmc/webui-vue",
      "check_days": 2,
      "max_results": 100
    },
    {
      "name": "openbmc/bmcweb",
      "check_days": 2,
      "max_results": 100
    },
    {
      "name": "openbmc/phosphor-webui",
      "check_days": 7,
      "max_results": 50
    }
  ]
}
```

### Change the reporting period

Edit [`config.json`](config.json):

```json
{
  "check_days": 14
}
```

### Change the schedule

For the daily workflow, edit [`.github/workflows/daily-monitor.yml`](.github/workflows/daily-monitor.yml):

```yaml
schedule:
  - cron: '5 7 * * *'
```

For the weekly workflow, edit [`.github/workflows/weekly-monitor.yml`](.github/workflows/weekly-monitor.yml):

```yaml
schedule:
  - cron: '0 9 * * 1'
```

### Cron examples

- `5 7 * * *` — Every day at 7:05 AM UTC
- `5 7 * * 1` — Every Monday at 7:05 AM UTC
- `5 7 * * 1,5` — Every Monday and Friday at 7:05 AM UTC
- `5 7 1 * *` — First day of every month at 7:05 AM UTC
- `0 9 * * 1` — Every Monday at 9:00 AM UTC

### Additional customization ideas

Potential enhancements supported by the current design include:

- Adding custom change filters by author, path, or review status
- Adjusting report formatting in [`monitor.py`](monitor.py)
- Sending reports to multiple channels or multiple recipients

## Troubleshooting

### No report generated

- Check console logs or workflow logs
- Verify Gerrit URL and project name in [`config.json`](config.json)
- Ensure GitHub Actions is enabled if using workflows

### Empty report

- This may be normal if there was no activity in the selected period
- Increase `check_days` in [`config.json`](config.json)

### Gerrit API errors

Possible causes:

1. Temporary Gerrit outage
2. Invalid project configuration
3. Network issues

Suggested actions:

- Open the configured Gerrit project URL in a browser
- Verify the configured project name
- Retry later if the service appears unavailable

### Slack not working

- Confirm `SLACK_WEBHOOK_URL` is set correctly
- Check whether the webhook has been revoked
- Verify network connectivity
- Remember that Slack is optional and report generation still works without it

### Email not sending

Common causes:

- Wrong SMTP host or port
- Using a normal Gmail password instead of an app password
- Missing 2-Step Verification for Gmail
- Typo in sender or recipient address
- Email delivered to spam

Suggested actions:

- Verify SMTP settings
- Remove spaces from Gmail app passwords
- Check spam or junk folders
- Review the workflow logs for the weekly job

### GitHub Actions workflow not running

Possible causes:

1. Workflow disabled
2. Required secrets missing
3. Repository limitations or billing constraints

Suggested actions:

- Review the Actions tab for errors
- Trigger the workflow manually once
- Re-check all required secrets

## Example Gerrit Targets

This monitor is generic and can be used for many Gerrit-hosted repositories.

Example project targets include:

- `openbmc/webui-vue`
- `openbmc/bmcweb`
- `openbmc/phosphor-webui`
- `company/platform-ui`
- `team/internal-service`

## Use Cases

- Team activity summaries
- Code review tracking
- Release planning
- Ongoing project visibility
- Onboarding support for new contributors

## Support

If something is not working:

1. Review workflow logs in GitHub Actions
2. Check local command output
3. Verify Gerrit access
4. Validate Slack or SMTP credentials
5. Run [`python monitor.py`](monitor.py:1) locally to reproduce the issue

## Project Status

**Status:** Production ready

Implemented capabilities include:

- Gerrit API integration
- Markdown report generation
- Slack webhook integration
- Weekly email support
- GitHub Actions automation
- Error handling and logging
- Test utilities and setup helpers

## Next Steps

1. Run the monitor locally or through GitHub Actions
2. Verify that the report file is generated
3. Configure Slack and/or email if needed
4. Adjust the schedule and reporting window for your team

## GERRIT_DAILY_REPORT

# 📊 WebUI Gerrit Activity Report
**Generated:** 2026-04-11 09:34:04 UTC
**Project:** [openbmc/webui-vue](https://gerrit.openbmc.org/q/project:openbmc/webui-vue)
**Period:** 2026-04-09 to 2026-04-11 (2 days)
**Total Changes:** 5

---

## 🔍 Open MRs (4)

### [Display user privilege in profile settings](https://gerrit.openbmc.org/c/89123)
- **Change #:** 89123
- **Author:** Aravinth Sri Krishna Raja Raghavan
- **Updated:** 2026-04-10 13:37:57.000000000

### [Fix UI alignment issues on Logs and Dumps pages](https://gerrit.openbmc.org/c/87222)
- **Change #:** 87222
- **Author:** Aravinth Sri Krishna Raja Raghavan
- **Updated:** 2026-04-10 10:24:24.000000000

### [Fix redirect handling to prevent Redfish logout](https://gerrit.openbmc.org/c/87472)
- **Change #:** 87472
- **Author:** Aravinth Sri Krishna Raja Raghavan
- **Updated:** 2026-04-10 10:14:34.000000000

### [Fix SOL console frozen rows, scrollbar, and text selection](https://gerrit.openbmc.org/c/88367)
- **Change #:** 88367
- **Author:** Jason Westover
- **Updated:** 2026-04-09 00:45:43.000000000

## 🚧 Work In Progress (1)

### [Display UserType in the user profile](https://gerrit.openbmc.org/c/88397)
- **Change #:** 88397
- **Author:** Aravinth Sri Krishna Raja Raghavan
- **Updated:** 2026-04-10 14:07:14.000000000

---

*Report generated by WebUI Gerrit Activity Monitor*
*Repository: https://gerrit.openbmc.org/q/project:openbmc/webui-vue*

## License

MIT License