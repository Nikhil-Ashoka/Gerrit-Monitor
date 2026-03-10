# 🧪 Testing Instructions - Email Functionality

## What Has Been Set Up

I've configured the Gerrit Monitor to send **weekly email reports** to **a.nikhil@ibm.com**. Here's what's ready:

### ✅ Files Created/Modified:

1. **monitor.py** - Added `EmailNotifier` class with HTML email support
2. **.env** - Email configuration template (needs your credentials)
3. **.env.example** - Updated with email settings documentation
4. **test_email.py** - Test script to send immediate email
5. **.github/workflows/weekly-monitor.yml** - Weekly automation (Mondays at 2:30 PM IST)
6. **EMAIL_SETUP.md** - Comprehensive setup guide
7. **QUICK_START_EMAIL.md** - Quick reference guide
8. **setup_email.sh** - Setup helper script

## 🎯 To Test Email Functionality NOW

### Option 1: Quick Test (Recommended)

1. **Edit the `.env` file** with your email credentials:
   ```bash
   nano .env
   # or
   code .env
   ```

2. **Update these lines:**
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   TO_EMAILS=a.nikhil@ibm.com
   ```

3. **Run the test:**
   ```bash
   python test_email.py
   ```

4. **Check the inbox** at a.nikhil@ibm.com

### Option 2: Using Gmail (Step-by-Step)

1. **Get Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Enable 2-Step Verification if not already enabled
   - Create app password for "Mail"
   - Copy the 16-character password

2. **Update .env file:**
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop  # Your 16-char app password
   FROM_EMAIL=your-email@gmail.com
   TO_EMAILS=a.nikhil@ibm.com
   ```

3. **Test it:**
   ```bash
   python test_email.py
   ```

### Expected Output:

```
✅ Email settings found
SMTP Host: smtp.gmail.com
SMTP Port: 587
From: your-email@gmail.com
To: a.nikhil@ibm.com
Monitoring project: openbmc/webui-vue
Checking last 7 days
Fetching changes from Gerrit...
Found X changes
✅ Report generated successfully!
📄 Report saved to: GERRIT_DAILY_REPORT.md

============================================================
Sending test email...
============================================================

✅ TEST EMAIL SENT SUCCESSFULLY!
============================================================
Check your inbox at: a.nikhil@ibm.com
If you don't see it, check your spam folder.
```

## 📧 What the Email Contains

The email will include:
- **Subject:** 📊 [TEST] Gerrit Weekly Activity Report - openbmc/webui-vue - 2026-03-10
- **Format:** Beautiful HTML with styling
- **Content:**
  - Summary statistics (total changes)
  - ✅ Merged changes (with author, lines changed)
  - 🔍 Open changes awaiting review
  - 🚧 Work in progress items
  - ❌ Abandoned changes
  - Direct clickable links to each change

## 🤖 Weekly Automation Setup

Once testing works, set up GitHub Actions for weekly automation:

### 1. Add GitHub Secrets

Go to: **Repository Settings** → **Secrets and variables** → **Actions**

Add these secrets:
- `SMTP_HOST` = `smtp.gmail.com`
- `SMTP_PORT` = `587`
- `SMTP_USER` = Your email address
- `SMTP_PASSWORD` = Your app password
- `FROM_EMAIL` = Your email address
- `TO_EMAILS` = `a.nikhil@ibm.com`

### 2. Enable Workflow

The workflow is already created at `.github/workflows/weekly-monitor.yml`

It will automatically:
- Run every **Monday at 9:00 AM UTC** (2:30 PM IST)
- Generate report for **last 7 days**
- Send email to **a.nikhil@ibm.com**
- Save report to repository

### 3. Manual Trigger (Optional)

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Select **Weekly Gerrit Monitor**
3. Click **Run workflow**

## 🔍 Troubleshooting

### Email Not Sending?

1. **Check credentials:**
   ```bash
   python test_email.py
   ```
   Look for error messages

2. **Common issues:**
   - Using regular password instead of app password
   - 2-Step Verification not enabled
   - Wrong SMTP host/port
   - Typo in email address

3. **Gmail specific:**
   - Must use App Password (16 characters)
   - Must have 2-Step Verification enabled
   - Remove spaces from app password

### Email in Spam?

1. Add sender to contacts
2. Mark as "Not Spam"
3. Create filter to always deliver to inbox

## 📊 Current Configuration

- **Recipient:** a.nikhil@ibm.com
- **Schedule:** Weekly (Mondays at 2:30 PM IST)
- **Coverage:** Last 7 days of activity
- **Project:** openbmc/webui-vue
- **Format:** HTML email + Plain text fallback

## 🎨 Customization

### Change Schedule

Edit `.github/workflows/weekly-monitor.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC (2:30 PM IST)
```

Examples:
- `0 9 * * 5` - Every Friday
- `0 0 1 * *` - First day of month
- `0 9 * * 1,5` - Monday and Friday

### Change Coverage Period

Edit `.env`:
```
CHECK_DAYS=7  # Change to 14 for bi-weekly, 30 for monthly
```

### Add More Recipients

Edit `.env`:
```
TO_EMAILS=a.nikhil@ibm.com,another@email.com,third@email.com
```

## 📝 Next Steps

1. ✅ Configure `.env` with your email credentials
2. ✅ Run `python test_email.py` to test
3. ✅ Check a.nikhil@ibm.com inbox
4. ✅ Add GitHub Secrets for automation
5. ✅ Wait for Monday or manually trigger workflow

---

**Ready to test?** Run: `python test_email.py` 🚀

For detailed help, see [EMAIL_SETUP.md](EMAIL_SETUP.md)