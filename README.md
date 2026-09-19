# Job Application Tracker

A Python-based email monitor that scans your Gmail inbox for job opportunities and application updates, using IMAP.

## What It Does

- Connects securely to Gmail via IMAP
- Scans recent unread emails for job-related keywords (e.g. "developer", "remote", "hiring", "software engineer")
- Detects and displays matching emails with sender, subject, and a preview
- Logs found opportunities to `job_offers_log.txt`
- Supports a continuous monitoring mode (checks every 5 minutes)

## Setup

1. Enable IMAP in your Gmail settings (Settings → Forwarding and POP/IMAP)
2. Generate a Gmail App Password (requires 2-Step Verification enabled)
3. Set environment variables:
   ```bash
   export GMAIL_ADDRESS="your_email@gmail.com"
   export GMAIL_APP_PASSWORD="your_app_password"
