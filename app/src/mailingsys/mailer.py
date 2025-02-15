import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.settings import mail_settings


def send_mail(receiver_email: str, subject: str, message: str):
    email_address = mail_settings.mail_username
    email_password = mail_settings.mail_password
    smtp_server = mail_settings.mail_host
    smtp_port = mail_settings.mail_port

    sender_email = email_address

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))
    smtp_port_str = int(smtp_port)

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port_str) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        # Handle any exceptions or errors that may occur during email sending
        print(f"Failed to send email: {e}")
