import smtplib
from email.message import EmailMessage
from .config_loader import get_config  # File 2
from dotenv import load_dotenv
import os

load_dotenv()

def send_alert_to_all(ticker, decision):
    # 1. Load credentials from .env
    sender_email = get_config("GMAIL_USER")
    app_password = get_config("GMAIL_APP_PASSWORD")

    recipients = [
        get_config("PERSONAL_PHONE"),
        "rohithsadanala1@gmail.com"
    ]

    # 2. Create the message content
    body = f"AI ALERT: {ticker}\nDECISION: {decision}"

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "StockBot Update"
    msg['From'] = sender_email
    msg['To'] = recipients

    # 3. Connect to Gmail and Send (The "POST" equivalent for Email)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return False

if __name__ == "__main__":
    test_result = send_alert_to_all("TEST", "BUY - Ready for File 8!")
    if test_result:
        print("✅ Check your iPhone!, GMAIL The message should arrive shortly.")