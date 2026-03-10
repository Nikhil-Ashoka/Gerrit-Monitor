# 🚀 Quick Start - Email Testing

Send a test email to **a.nikhil@ibm.com** in 3 simple steps!

## Step 1: Configure Email Settings

Edit the `.env` file and update these lines:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com          # ← Your email
SMTP_PASSWORD=your-app-password-here    # ← Your app password
FROM_EMAIL=your-email@gmail.com         # ← Your email
TO_EMAILS=a.nikhil@ibm.com             # ✅ Already set!
```

### Getting Gmail App Password:
1. Go to: https://myaccount.google.com/apppasswords
2. Create new app password for "Mail"
3. Copy the 16-character password
4. Paste it in `SMTP_PASSWORD`

## Step 2: Test the Email

Run the test script:

```bash
python test_email.py
```

## Step 3: Check Inbox

Check **a.nikhil@ibm.com** for the test email!

Subject: `📊 [TEST] Gerrit Weekly Activity Report - openbmc/webui-vue - YYYY-MM-DD`

---

## 📅 Weekly Automation

Once testing works, the weekly report will automatically:
- Run every **Monday at 2:30 PM IST** (9:00 AM UTC)
- Cover the **last 7 days** of activity
- Send to **a.nikhil@ibm.com**

### Setup GitHub Secrets (for automation):

1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `SMTP_HOST` → `smtp.gmail.com`
   - `SMTP_PORT` → `587`
   - `SMTP_USER` → Your email
   - `SMTP_PASSWORD` → Your app password
   - `FROM_EMAIL` → Your email
   - `TO_EMAILS` → `a.nikhil@ibm.com`

### Manual Trigger:

Go to **Actions** → **Weekly Gerrit Monitor** → **Run workflow**

---

## 🆘 Troubleshooting

**Email not sending?**
```bash
# Check your settings
python test_email.py
```

**Common fixes:**
- Use App Password, not regular password
- Enable 2-Step Verification in Gmail
- Check spam folder
- Verify SMTP settings

---

**Need more help?** See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed instructions.