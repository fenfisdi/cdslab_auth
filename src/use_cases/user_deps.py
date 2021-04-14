import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import email_config


def send_email(email: str, main_message: str):
    """
        Sends registration email to the given address.

        Builds path for the user and add the tokenized email,
        then uses MIMEMultipart to add the welcome message containing the
        image and the link to finish the registration process.
        connect to the google server and using the user's credentials
        send the message

        Parameters
        ----------
        email : str
            User's email
    """
    msg = MIMEMultipart()

    message = email_config.get("MESSAGE")
    password = email_config.get("PASSWORD")
    msg["From"] = email_config.get("FROM_EMAIL")
    msg["To"] = email
    msg["Subject"] = email_config.get("SUBJECT")
    msg.attach(MIMEText(email_config.get("LOGO"), "html"))

    fp = open(email_config.get("LOGO_PATH"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()

    msg_img.add_header("Content-ID", "<cdslab_auth_logo>")
    msg.attach(msg_img)
    msg.attach(MIMEText(message, "html"))
    msg.attach(
        MIMEText(f"<center><br><b>{main_message}</b></br></center>", "html")
    )

    server = smtplib.SMTP(email_config.get("SERVER"))
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
