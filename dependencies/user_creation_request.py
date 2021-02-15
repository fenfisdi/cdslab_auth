import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config

def send_registration_email(email: str):
    msg = MIMEMultipart()
    message = config.send_registration_email.message()
    password = config.send_registration_email.password()
    msg["From"] = config.send_registration_email.from_email()
    msg["To"] = email
    msg["Subject"] = config.send_registration_email.subject()
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP(config.send_registration_email.server())
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    return config.send_registration_email.response() + msg["To"]
    
    