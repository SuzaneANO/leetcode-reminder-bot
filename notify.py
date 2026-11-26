import os
import smtplib
from email.message import EmailMessage


def notify_by_email(username: str, recipient_email: str) -> None:
    smtp_host = os.environ.get("BREVO_SMTP_HOST", "smtp-relay.brevo.com")
    smtp_port = int(os.environ.get("BREVO_SMTP_PORT", "587"))
    smtp_user = os.environ["BREVO_SMTP_USER"]
    smtp_key = os.environ["BREVO_SMTP_KEY"]
    sender_email = os.environ.get("BREVO_SENDER_EMAIL", smtp_user)

    msg = EmailMessage()
    msg["Subject"] = f"LeetCode Reminder for {username}"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(
        f"Hi {username},\n\n"
        "You haven't completed an Accepted LeetCode submission yet today. "
        "Time to solve a problem!"
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_key)
        server.send_message(msg)