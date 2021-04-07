import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from passlib.context import CryptContext

from source.config import email_config, settings, secrets
from source.dependencies.qr_deps import generate_key_qr
from source.dependencies.token_deps import generate_token_jwt
from source.models.user import User, StoredUser

context = CryptContext(
    schemes=[secrets.get("CRYPTOCONTEXT_SCHEM")],
    deprecated=secrets.get("CRYPTOCONTEXT_DEPRECATED")
)


def send_email(email: str) -> str:
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
    key_email = generate_token_jwt({"email": email})["access_token"]

    applicant_link = f'{settings["DOMAIN"]}{settings["REGISTER_PATH"]}/{key_email}'

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
    msg.attach(MIMEText(applicant_link, "html"))

    server = smtplib.SMTP(email_config.get("SERVER"))
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()


def get_hash_password(password: str) -> str:
    """
        Take the user password and hash it

        Parameters
        ----------
        password: dict
            Password taken from User class

        Return
        ----------
        Method: str
            Password hashed by the passlib library
    """
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
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


def transform_props_to_user(user: User):
    """
        Construct model from User class to store in database

        Parameters
        ----------
        user: Pydantic class
            Inherits the properties of User

        Return
        ----------
        StoredUser: Pydantic class
            Model to store in database
    """
    hashed_password = get_hash_password(user.password)
    return StoredUser(**user.dict(),
                      hashed_password=hashed_password,
                      key_qr=generate_key_qr())
