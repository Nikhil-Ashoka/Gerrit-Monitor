# 🔐 GitHub Secrets Setup - Required for Automatic Emails

## ⚠️ Important: One-Time Setup Required

To receive automatic weekly emails, you need to add your email credentials to GitHub Secrets. This is a **one-time setup** that takes about 2 minutes.

## 📋 Step-by-Step Instructions

### Step 1: Go to Repository Settings

1. Open your GitHub repository in a browser
2. Click on **"Settings"** tab (top right)
3. In the left sidebar, click **"Secrets and variables"**
4. Click **"Actions"**

### Step 2: Add Email Secrets

Click **"New repository secret"** and add each of these secrets one by one:

#### Secret 1: SMTP_HOST
- **Name:** `SMTP_HOST`
- **Value:** `smtp.gmail.com`
- Click "Add secret"

#### Secret 2: SMTP_PORT
- **Name:** `SMTP_PORT`
- **Value:** `587`
- Click "Add secret"

#### Secret 3: SMTP_USER
- **Name:** `SMTP_USER`
- **Value:** `nikhilashokaa@gmail.com`
- Click "Add secret"

#### Secret 4: SMTP_PASSWORD
- **Name:** `SMTP_PASSWORD`
- **Value:** `qjnq zupu nxcb qean` (your Gmail app password)
- Click "Add secret"

#### Secret 5: FROM_EMAIL
- **Name:** `FROM_EMAIL`
- **Value:** `nikhilashokaa@gmail.com`
- Click "Add secret"

#### Secret 6: TO_EMAILS
- **Name:** `TO_EMAILS`
- **Value:** `rajivs12@in.ibm.com,a.nikhil@ibm.com,Vedangi.Mittal@ibm.com,tiwari.nishant@ibm.com`
- Click "Add secret"

### Step 3: Verify Setup

After adding all 6 secrets, you should see them listed (values will be hidden for security):
- ✅ SMTP_HOST
- ✅ SMTP_PORT
- ✅ SMTP_USER
- ✅ SMTP_PASSWORD
- ✅ FROM_EMAIL
- ✅ TO_EMAILS

## 🎯 What Happens Next?

### Automatic Weekly Emails
- **When:** Every Monday at 9:00 AM UTC (2:30 PM IST)
- **To:** a.nikhil@ibm.com, Vedangi.Mittal@ibm.com, tiwari.nishant@ibm.com
- **Content:** Last 7 days of Gerrit activity
- **No further action needed!**

### Manual Testing (Optional)
You can manually trigger the workflow to test:
1. Go to **"Actions"** tab in GitHub
2. Click **"Weekly Gerrit Monitor"**
3. Click **"Run workflow"** button
4. Select branch and click **"Run workflow"**
5. Wait 1-2 minutes and check your email!

## 🔒 Security Notes

- Secrets are encrypted and never exposed in logs
- Only GitHub Actions can access these secrets
- You can update or delete secrets anytime
- Never commit the `.env` file to GitHub (it's in `.gitignore`)

## ❓ FAQ

**Q: Do I need to do this setup again?**  
A: No! This is a one-time setup. Once configured, emails will send automatically every Monday.

**Q: Can I change the recipients later?**  
A: Yes! Just update the `TO_EMAILS` secret in GitHub Settings.

**Q: What if I change my Gmail password?**  
A: You'll need to generate a new app password and update the `SMTP_PASSWORD` secret.

**Q: Will this work if my repository is private?**  
A: Yes! GitHub Actions work for both public and private repositories.

## ✅ Quick Checklist

Before the first automatic email, make sure:
- [ ] All 6 secrets are added to GitHub
- [ ] The `.github/workflows/weekly-monitor.yml` file is committed
- [ ] The `monitor.py` file with email functionality is committed
- [ ] You've tested manually and received the email successfully

---

**Once you complete this setup, you'll automatically receive weekly emails every Monday!** 🎉

Need help? Check the GitHub Actions logs in the "Actions" tab if emails don't arrive.