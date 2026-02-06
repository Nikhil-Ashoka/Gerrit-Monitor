# Gerrit Daily Activity Monitor

Automated monitoring system for tracking daily activities in the OpenBMC WebUI Vue Gerrit repository and generating detailed reports.

## Features

- Monitors https://gerrit.openbmc.org/q/project:openbmc/webui-vue for weekly activities
- Fetches changes (commits, reviews, merges) from the past week
- **Generates a detailed markdown report (GERRIT_WEEKLY_REPORT.md)** with all changes
- Optionally posts formatted updates to a Slack channel via webhook (when configured)
- Runs automatically every week using GitHub Actions (or can be run locally with cron)
- No external dependencies beyond Python standard library and requests

## Setup

### Prerequisites

- Python 3.8 or higher
- A Slack workspace with webhook access

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd gerrit-monitor
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up your Slack webhook:
   - Go to https://api.slack.com/messaging/webhooks
   - Create a new webhook for your desired channel
   - Copy the webhook URL

4. Configure the application (optional for Slack):
   - Copy `.env.example` to `.env`
   - Add your Slack webhook URL to `.env` (optional - only needed if you want Slack notifications)

### Configuration

Edit `config.json` to customize:
- `gerrit_url`: The Gerrit instance URL
- `project`: The project to monitor
- `check_days`: Number of days to look back (default: 7)

## Usage

### Manual Execution

Run the monitor manually:
```bash
python monitor.py
```

### Automated Execution (GitHub Actions)

The repository includes a GitHub Actions workflow that runs automatically **every day at 7:05 AM UTC (12:35 PM IST)**.

To enable:
1. Fork this repository
2. Push to GitHub
3. Enable GitHub Actions in the Actions tab
4. (Optional) To enable Slack notifications:
   - Go to Settings → Secrets and variables → Actions
   - Add a new secret named `SLACK_WEBHOOK_URL` with your webhook URL
5. The workflow will run automatically daily and generate GERRIT_WEEKLY_REPORT.md

### Automated Execution (Local Cron)

Add to your crontab to run every day at 12:35 PM IST:
```bash
5 7 * * * cd /path/to/gerrit-monitor && python monitor.py
```

## Output Format

The generated report (GERRIT_WEEKLY_REPORT.md) includes:
- Report metadata (date, project, period)
- Total number of changes in the week
- **Merged changes** with code statistics (+/- lines)
- **Open changes** awaiting review
- **Work in progress** changes
- **Abandoned changes**
- Direct links to each change in Gerrit

If Slack webhook is configured, a formatted message is also sent to Slack with the same information.

## Troubleshooting

- **No report generated**: Check the logs for errors, verify Gerrit URL and project name are correct
- **Empty reports**: Normal if there's no activity in the specified period
- **Slack not working**: Verify SLACK_WEBHOOK_URL is set correctly (Slack is optional)
- **API errors**: Gerrit API might be temporarily unavailable, the script will retry

## Notes

- **Slack is optional**: The monitor will generate a markdown report regardless of Slack configuration
- **Report location**: GERRIT_WEEKLY_REPORT.md is created in the project root directory
- **Schedule**: Runs **every day** at 7:05 AM UTC (12:35 PM IST)
- **Report period**: By default, checks the last 7 days of activity (configurable in config.json)

## License

MIT License