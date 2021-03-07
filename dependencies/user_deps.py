import smtplib
import jsoncfg

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jose import jwt
from dotenv import dotenv_values

from models import user

send_registration_email = jsoncfg.load_config('send_email.cfg')
secrets = dotenv_values(".secrets")
settings = dotenv_values(".env")

def tokenize_email(user: user.applicant_user) -> str:
    """
    Tokenize the email taken the applicant_user class as a parameter

    Parameters
    ----------
    user : dict 
            Object type applicant_user

    Returns
    ----------
    str
        The email tokenized by jwt method
    """
    if type(user.email) is not str:
            raise ValueError("Invalid type")
        
    email_to_encode = user.dict()
    tokenized_email = jwt.encode(email_to_encode, secrets["SECRET_KEY"], algorithm=secrets["ALGORITHM"])
    return tokenized_email


def send_email(user: user.applicant_user) -> str:
        """
        Send registration email to the adress entered by the user


        Build the path that will be sent to the user and add the tokenized email, 
        then use the MIMEMultipart library to pack the welcome message, 
        the image and the link to the registration, finally it connects with 
        the google server and with the credentials of the specified email send the message


        Parameters
        ----------
        user : dict 
                Object type applicant_user

        Returns
        ----------
        str
            The confirmation with the email is sended

        """
        key_email = tokenize_email(user)
        key_email = f'{"/"}{key_email}'
        applicant_key = f'{settings["DOMAIN"]}{settings["APPLICANT_PATH"]}{key_email}'
        msg = MIMEMultipart()

        message = send_registration_email.message()
        password = send_registration_email.password()
        msg["From"] = send_registration_email.from_email()
        msg["To"] = user.email
        msg["Subject"] = send_registration_email.subject()
        msg.attach(MIMEText(send_registration_email.logo(), "html"))

        fp = open(send_registration_email.logo_path(),"rb")
        msgImg = MIMEImage(fp.read())
        fp.close()

        msgImg.add_header("Content-ID", "<cdslab_auth_logo>")
        msg.attach(msgImg)
        msg.attach(MIMEText(message, "html"))
        msg.attach(MIMEText(applicant_key,"html"))

        server = smtplib.SMTP(send_registration_email.server())
        server.starttls()
        server.login(msg["From"], password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()

        return send_registration_email.response() + msg["To"]