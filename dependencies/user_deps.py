import smtplib
import jsoncfg

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from passlib.context import CryptContext
from dotenv import dotenv_values

from models import user
from dependencies import qr_deps, token_deps


send_registration_email = jsoncfg.load_config('send_email.cfg')
secrets = dotenv_values(".secrets")
settings = dotenv_values(".env")

context = CryptContext(schemes=[secrets['CRYPTOCONTEXT_SCHEM']],
                       deprecated=secrets['CRYPTOCONTEXT_DEPRECATED'])


def send_email(email: str) -> str:
    """
    Send registration email to the adress entered by the user


    Build the path that will be sent to the user and add the tokenized email, 
    then use the MIMEMultipart library to pack the welcome message, 
    the image and the link to the registration, finally it connects with 
    the google server and with the credentials of the specified email send the message


    Parameters
    ----------
    email : str
            Who receives the sent email

    """
    key_email = token_deps.generate_token_jwt({'email': email})
    key_email = key_email['access_token']
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


def get_hash_password(password: user.user_in) -> str:
    """
    Take the user password and hash it

    Parameters
    ----------
    password: dict
            The password taked from user_in class

    Return
    ----------
    hashed_passoword: str
            The password hashed by the passlib library
    """
    hashed_password = context.hash(password)
    return hashed_password


def verify_passowrd(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the password entered by the user and the hassed password in the database
    match

    Parameters
    ----------
    plain_password: str
            String entered by the user in the authentication step
    hashed_password: str
            The password hashed saved in the database associated with the user

    Return
    ----------
    is_verify: bool
            If the password match returns True otherwise returns false
    """
    is_verify = context.verify(plain_password, hashed_password)
    return is_verify


def transform_props_to_user(user_in: user.user_in):
    """
    Takes the user_in class and contruct the model that will be saved on the database

    Parameters
    ----------
    user_in: Pydantic class
            Inherits the properties of user_in

    Return
    ----------
    user_in_db: Pydantic class
            The model that will be saved in the databases merging the attributes in user_in class
            and user_in_db class
    """
    hashed_password = get_hash_password(user_in.password)
    user_in_db = user.user_in_db(**user_in.dict(),
                                 hashed_password=hashed_password,
                                 key_qr=generate_key_qr(),
                                 )
    return user_in_db
    hashed_password = get_hash_password(user.password)
    return user_in_db(**user.dict(),
                        hashed_password=hashed_password,
                        key_qr=generate_key_qr()                    
                     )
     
