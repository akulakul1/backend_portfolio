from email.utils import formataddr

@app.post("/send-email")
async def send_email(data: EmailSchema):
    try:
        sender = os.getenv("EMAIL_SENDER")        # Your email, for SMTP auth
        receiver = os.getenv("EMAIL_RECEIVER")    # Your email, to receive messages
        password = os.getenv("EMAIL_APP_PASSWORD")

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = f"New message from {data.first} {data.last}"
        msg.add_header('Reply-To', data.email)  # Add visitor's email as Reply-To

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
