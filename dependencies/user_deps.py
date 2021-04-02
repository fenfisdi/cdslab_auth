import smtplib
import jsoncfg

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from passlib.context import CryptContext
from dotenv import dotenv_values

from models.user import user_in, user_in_db
from dependencies.qr_deps import generate_key_qr
from dependencies.token_deps import generate_token_jwt

send_registration_email = jsoncfg.load_config('send_email.cfg')
secrets = dotenv_values(".secrets")
settings = dotenv_values(".env")

context = CryptContext(schemes=[secrets['CRYPTOCONTEXT_SCHEM']],
                       deprecated=secrets['CRYPTOCONTEXT_DEPRECATED'])

def send_email(email: str) -> str:
    """
        Send registration email to the given address.

        Build path for the user and add the tokenized email,
        use MIMEMultipart to add the welcome message containing the
        image and the link to finish the registration process,
        connect to the google server and using the user's credentials
        send the message

        Parameters
        ----------
        email : str
            User's email
    """

    key_email = token_deps.generate_token_jwt({'email': email})['access_token']

    applicant_key = f'{settings["DOMAIN"]}{settings["REGISTER_PATH"]}/{key_email}'
    msg = MIMEMultipart()

    message = send_registration_email.message()
    password = send_registration_email.password()
    msg["From"] = send_registration_email.from_email()
    msg["To"] = email
    msg["Subject"] = send_registration_email.subject()
    msg.attach(MIMEText(send_registration_email.logo(), "html"))

    fp = open(send_registration_email.logo_path(), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()

    msg_img.add_header("Content-ID", "<cdslab_auth_logo>")
    msg.attach(msg_img)
    msg.attach(MIMEText(message, "html"))
    msg.attach(MIMEText(applicant_key, "html"))

    server = smtplib.SMTP(send_registration_email.server())
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()


def get_hash_password(password: user_in) -> str:
    """
        Take the user password and hash it

        Parameters
        ----------
        password: dict
            Password taken from user_in class

        Return
        ----------
        Method: str
            Password hashed by the passlib library
    """
    return context.hash(password)


def verify_passowrd(plain_password: str, hashed_password: str) -> bool:
    """
        Compare stored and entered passwords

        Parameters
        ----------
        plain_password: str
            String used to authenticate
        hashed_password: str
            String with the respective stored password

        Return
        ----------
        Method: bool
            True or False whether passwords match
    """
    return context.verify(plain_password, hashed_password)


def transform_props_to_user(user: user_in):
    """
        Construct model from user_in class to store in database

        Parameters
        ----------
        user_in: Pydantic class
            Inherits the properties of user_in

        Return
        ----------
        user_in_db: Pydantic class
            Model to store in database
    """
    hashed_password = get_hash_password(user.password)
    return user_in_db(**user.dict(),
                      hashed_password=hashed_password,
                      key_qr=generate_key_qr())
