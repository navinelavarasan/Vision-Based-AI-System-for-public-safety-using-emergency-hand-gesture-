import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

def send_email_alert(image_path):
    # ===== EMAIL SETTINGS =====
    SENDER_EMAIL = "navinelavarasanofficial@gmail.com"
    RECEIVER_EMAIL = "navinelavarasan28@gmail.com"
    APP_PASSWORD = "uqzj paxz vsxl olvt"  # Gmail App Password

    msg = EmailMessage()
    msg["Subject"] = "🚨 EMERGENCY ALERT DETECTED"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    msg.set_content(
        f"""
EMERGENCY ALERT!

An emergency gesture was detected by the AI surveillance system.

Time: {current_time}

Please find the attached image for visual confirmation.
"""
    )

    # Attach image
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(image_path)

        msg.add_attachment(
            file_data,
            maintype="image",
            subtype="jpeg",
            filename=file_name
        )

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("[EMAIL SENT] Emergency alert delivered successfully.")

