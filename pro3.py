import smtplib
from email.mime.text import MIMEText

# Sender & Receiver
sender_email = "zeusmg2619@gmail.com"
receiver_email = "albinepeter2004@gmail.com"

# Use App Password here
app_password = "hhdu okvk llub rkpd"

# Mail content
subject = "Test Mail Forward"
body = "This is a test mail sent using Python."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

# Send mail
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, app_password)

server.sendmail(sender_email, receiver_email, msg.as_string())
server.quit()

print("Mail sent successfully 🚀")