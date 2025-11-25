import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
from app.utils.logging import log_info, log_error
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY="SUPER_SECRET_KEY_CHANGE_THIS"
serializer=URLSafeTimedSerializer(SECRET_KEY)

SMTP_EMAIL=os.getenv("SMTP_EMAIL")
SMTP_PASS=os.getenv("SMTP_PASS")

VERIFY_LINK_BASE="http://127.0.0.1:8000/verify/confirm"

def generate_token(email:str):
    return serializer.dumps(email,salt="email-confirm")


def confirm_token(token:str,expiration=3600):
    try:
        email=serializer.loads(token,salt="email-confirm",max_age=expiration)
        return email
    except Exception:
        return None
    
def send_verification_email(to_email:str):
    try:
        token=generate_token(to_email)
        verification_link=f"{VERIFY_LINK_BASE}?token={token}"

        subject="Email Verification - User Management API"
        body=f""" Hii {to_email},
        Please verify your email by clicking the link below:
        {verification_link}

        This link will expire in 1 hour..."""

        msg=MIMEText(body)
        msg["Subject"]=subject
        msg["From"]=SMTP_EMAIL
        msg["To"]=to_email

        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(SMTP_EMAIL,SMTP_PASS)
            server.sendmail(SMTP_EMAIL,to_email,msg.as_string())

        log_info(f"Verification email sent to {to_email}")
        return True,token
    except Exception as e:
        log_error(f"Failed to send email: {e}")
        return False,None
    
    
