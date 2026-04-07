import imaplib
import smtplib
import email
import time
import traceback

EMAIL = "zeusmg2619@gmail.com"
PASSWORD = "hhdu okvk llub rkpd"
FORWARD_TO = "albinepeter2004@gmail.com"

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def forward_mail(msg):
    try:
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL, PASSWORD)

        smtp.sendmail(EMAIL, FORWARD_TO, msg.as_string())
        smtp.quit()

        print(f"✅ Forwarded: {msg['Subject']}")

    except Exception as e:
        print("❌ Error while forwarding:", e)


def check_inbox():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, '(UNSEEN)')

        mail_ids = messages[0].split()

        if not mail_ids:
            print("📭 No new mails")

        for num in mail_ids:
            status, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            print(f"📩 New Mail: {msg['Subject']}")

            forward_mail(msg)

            
            mail.store(num, '+FLAGS', '\\Seen')

        mail.logout()

    except Exception as e:
        print("❌ Inbox check error:", e)
        traceback.print_exc()

print("🚀 Mail Auto Forward Service Started...\nPress CTRL + C to stop\n")

while True:
    check_inbox()
    time.sleep(20)   # check every 20 seconds