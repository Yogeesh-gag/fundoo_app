import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SMTP_SERVER=os.getenv("SMTP_SERVER","smtp.gmail.com")
    SMTP_PORT=int(os.getenv("SMTP_PORT",587))
    SMTP_EMAIL=os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
    FRONTEND_URL=os.getenv("FRONTEND_URL","http://127.0.0.1:8000")

settings=Settings()