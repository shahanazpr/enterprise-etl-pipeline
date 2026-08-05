import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, receiver):
    """
    Sends an email alert.
    SMTP configuration will be added later.
    """

    print(f"[EMAIL] To: {receiver}")
    print(subject)
    print(body)