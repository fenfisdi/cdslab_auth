import smtplib
import jsoncfg

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from passlib.context import CryptContext
from jose import jwt
from dotenv import dotenv_values

from db_connection import users
from models import user
from dependencies import qr_deps


send_registration_email = jsoncfg.load_config('send_email.cfg')
secrets = dotenv_values(".secrets")
settings = dotenv_values(".env")

context = CryptContext(schemes=[secrets['CRYPTOCONTEXT_SCHEM']], deprecated=secrets['CRYPTOCONTEXT_DEPRECATED'])

def tokenize_email(user: user.user_to_register) -> str:
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

    email_to_encode = {'email': user.email}
    tokenized_email = jwt.encode(email_to_encode, secrets["SECRET_KEY"], algorithm=secrets["ALGORITHM"])
    return tokenized_email

def send_email(user: user.user_to_register) -> str:
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

def verify_passowrd(plain_password: str, hashed_password: user.user_in_db) -> bool:
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
            inherits the properties of user_in

    Return
    ----------
    user_in_db: Pydantic class
            The model that will be saved in the databases merging the attributes in user_in class
            and user_in_db class
    """
    hashed_password = get_hash_password(user_in.password)
    user_in_db = user.user_in_db(**user_in.dict(), 
                hashed_password=hashed_password, 
                key_qr=qr_deps.generate_key_qr())
    
    return user_in_db