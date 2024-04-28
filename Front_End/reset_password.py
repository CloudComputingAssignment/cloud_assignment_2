import streamlit as st
import secrets
from email.mime.text import MIMEText
import smtplib


def generate_reset_token():
    return secrets.token_urlsafe(32)

def send_reset_email(email, token):
    
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    smtp_username = "cognimindai@gmail.com"
    smtp_password = ""

    
    sender_email = "cognimindai@gmail.com"
    recipient_email = email
    subject = "Password Reset Request"
    body = f'''
        To reset your password, click the following link:
        [Reset Link](http://localhost:8501/?page=reset&token={token})

        If you did not make this request, please ignore this email.
    '''

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = recipient_email

            server.sendmail(sender_email, recipient_email, msg.as_string())

        st.success("Password reset link sent to your email. Check your inbox or spam.")
    except Exception as e:
        st.error(f"Error sending email: {e}")