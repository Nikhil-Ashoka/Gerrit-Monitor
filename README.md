# Gerrit Weekly Activity Monitor

Automated monitoring system for tracking weekly activities in the OpenBMC WebUI Vue Gerrit repository and posting updates to Slack.

## Features

- Monitors https://gerrit.openbmc.org/q/project:openbmc/webui-vue for weekly activities
- Fetches changes (commits, reviews, merges) from the past week
- Posts formatted updates to a Slack channel via webhook
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

4. Configure the application:
   - Copy `.env.example` to `.env`
   - Add your Slack webhook URL to `.env`

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

The repository includes a GitHub Actions workflow that runs automatically every Monday at 9:00 AM UTC.

To enable:
1. Fork this repository
2. Go to Settings → Secrets and variables → Actions
3. Add a new secret named `SLACK_WEBHOOK_URL` with your webhook URL
4. The workflow will run automatically

### Automated Execution (Local Cron)

Add to your crontab to run every Monday at 9 AM:
```bash
0 9 * * 1 cd /path/to/gerrit-monitor && python monitor.py
```

## Output Format

The Slack message includes:
- Total number of changes in the week
- List of merged changes
- List of open changes awaiting review
- List of abandoned changes
- Direct links to each change

## Troubleshooting

- **No updates posted**: Check your Slack webhook URL and network connectivity
- **Empty reports**: Verify the Gerrit URL and project name are correct
- **API errors**: Gerrit API might be temporarily unavailable, the script will retry

## License

MIT License