from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "https://akul-r1gp47ogx-akulakul1s-projects.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailSchema(BaseModel):
    first: str
    last: str
    email: EmailStr
    subject: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Portfolio backend is running 🚀"}

@app.post("/send-email")
async def send_email(data: EmailSchema):
    try:
        sender = os.getenv("EMAIL_SENDER")
        receiver = os.getenv("EMAIL_RECEIVER")
        password = os.getenv("EMAIL_APP_PASSWORD")

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = f"New message from {data.first} {data.last}"

        body = f"""
Name: {data.first} {data.last}
Email: {data.email}
Subject: {data.subject}

Message:
{data.message}
        """

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        return {"error": str(e)}
