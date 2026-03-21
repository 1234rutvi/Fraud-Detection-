import smtplib
from email.mime.text import MIMEText

def send_email_alert(fraud_df):
    sender = "your_email@gmail.com"
    password = "zyaa htln clfr vxnt"   # 👈 IMPORTANT
    receiver = "your_email@gmail.com"

    subject = "🚨 Fraud Alert Detected!"

    body = f"""
    Suspicious transactions detected:

    {fraud_df.to_string(index=False)}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("EMAIL ERROR:", e)
        return False
