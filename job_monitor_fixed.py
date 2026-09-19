#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header
import subprocess   
import datetime
import os
import sys
import time
from datetime import timedelta

# ====== CONFIGURATION ======
EMAIL = "gmendoza4458@gmail.com"
PASSWORD = "lvorciltasntbusb"  
IMAP_SERVER = "imap.gmail.com"
# ==========================

KEYWORDS = [
    'software', 'developer', 'engineer', 'programmer',
    'entry level', 'junior', 'mid level', 'senior',
    'remote', 'work from home', 'wfh', 'hiring',
    'opportunity', 'position', 'role', 'career',
    'full stack', 'frontend', 'backend', 'devops',
    'python', 'java', 'javascript', 'react', 'node'
]

def decode_mime_header(header):
    if header is None:
        return ""
    decoded_parts = decode_header(header)
    result = []
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                part = part.decode(encoding or 'utf-8', errors='ignore')
            except:
                part = part.decode('utf-8', errors='ignore')
        result.append(str(part))
    return ''.join(result)

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                continue
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
                except:
                    continue
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            body = str(msg.get_payload())
    return body[:500]

def check_offers():
    try:
        print(f"\n🔍 Checking for job offers... [{datetime.datetime.now().strftime('%H:%M:%S')}]")
        
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")
        
        # Only scan emails from last 7 days
        date_7_days_ago = (datetime.datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(UNSEEN SINCE "{date_7_days_ago}")')
        
        if status != "OK" or not messages[0]:
            print("📭 No recent unread emails found.")
            mail.close()
            mail.logout()
            return []
        
        email_ids = messages[0].split()
        # Only process last 50 to avoid overloading
        if len(email_ids) > 50:
            email_ids = email_ids[-50:]
            
        print(f"📨 Found {len(email_ids)} recent unread emails, scanning...")
        
        matched_emails = []
        
        for e_id in email_ids:
            try:
                status, msg_data = mail.fetch(e_id, "(RFC822)")
                if status != "OK":
                    continue
                
                msg = email.message_from_bytes(msg_data[0][1])
                
                subject = decode_mime_header(msg["Subject"]).lower()
                sender = decode_mime_header(msg.get("From", "")).lower()
                
                # Skip your own emails
                if 'gmendoza4458@gmail.com' in sender:
                    continue
                
                # Check keywords
                matched = False
                matched_keywords = []
                for keyword in KEYWORDS:
                    if keyword in subject or keyword in sender:
                        matched = True
                        matched_keywords.append(keyword)
                
                if not matched:
                    continue
                
                body = get_email_body(msg)
                
                matched_emails.append({
                    'subject': subject,
                    'sender': sender,
                    'body': body,
                    'keywords': matched_keywords[:3]
                })
                
                # Display offer
                print("=" * 70)
                print("💼  JOB OPPORTUNITY DETECTED!")
                print("=" * 70)
                print(f"📧 From: {sender}")
                print(f"📝 Subject: {subject}")
                print(f"🔑 Keywords: {', '.join(matched_keywords[:5])}")
                print(f"\n📄 Preview:")
                print("-" * 70)
                print(body[:300] + "..." if len(body) > 300 else body)
                print("=" * 70)
                print()
                
            except Exception as e:
                continue
        
        mail.close()
        mail.logout()
        
        if matched_emails:
            with open('job_offers_log.txt', 'a') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Scan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Found {len(matched_emails)} offers\n")
                for offer in matched_emails:
                    f.write(f"  - From: {offer['sender']}\n")
                    f.write(f"    Subject: {offer['subject']}\n")
                f.write(f"{'='*60}\n")
            
            print(f"✅ Found {len(matched_emails)} job opportunities!")

        
        return matched_emails
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP Error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=" * 50)
    print("  💼 JOB OFFER MONITOR v2")
    print("=" * 50)
    print(f"  Email: {EMAIL}")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("  1. Check for offers now")
        print("  2. Continuous mode (check every 5 minutes)")
        print("  3. Show last offers found")
        print("  4. Exit")
        
        choice = input("\nChoose (1-4): ").strip()
        
        if choice == "1":
            check_offers()
        elif choice == "2":
            print("\n🔄 Running continuously (Ctrl+C to stop)")
            try:
                while True:
                    check_offers()
                    print(f"\n⏰ Next check in 5 minutes...")
                    time.sleep(300)
            except KeyboardInterrupt:
                print("\n\n⏹️ Stopped")
        elif choice == "3":
            if os.path.exists('job_offers_log.txt'):
                with open('job_offers_log.txt', 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    print("\n📋 Recent offers:")
                    print("-" * 50)
                    print('\n'.join(lines[-30:]))
            else:
                print("\n📭 No offers logged yet.")
        elif choice == "4":
            print("\n👋 Goodbye! Happy job hunting!")
            sys.exit(0)
        else:
            print("❌ Invalid choice")
        
        if choice != "2":
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
