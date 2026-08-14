import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email(subject, body, receiver=None):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")

    if receiver is None:
        receiver = os.getenv("EMAIL_RECEIVER")

    if not username or not password:
        print("⚠ SMTP credentials not configured.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = receiver

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(username, receiver, msg.as_string())

        print("✅ Email notification sent.")

    except Exception as e:
        print(f"❌ Email notification failed: {e}")