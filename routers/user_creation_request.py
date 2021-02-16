import smtplib
import os
import secrets
import settings

from fastapi import HTTPException, APIRouter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from passlib.context import CryptContext

from models import user
from db_conection import users
from config import config


def hash_email(email: str):
    """hash the email taken the applicant_user class as a parameter

    Keywords arguments:
    email -- the vaule of email field in the applicant_user class
    """
    crypto_context = CryptContext(
        schemes=[secrets.crypto_context_schem], 
        deprecated=[secrets.crypto_context_deprecated])
    return crypto_context.hash(email)

def send_registration_email(email: str):
    """Send registration email to the adress entered by the user

    Keywords arguments:
    email -- the value of email field in the applicant_user class
    """
    domain = settings.domain
    key_email = hash_email(email)
    key_email = '/'+key_email
    applicant_key = domain+settings.applicant_path+key_email
    msg = MIMEMultipart()
    message = config.send_registration_email.message()
    password = config.send_registration_email.password()
    msg["From"] = config.send_registration_email.from_email()
    msg["To"] = email
    msg["Subject"] = config.send_registration_email.subject()
    msg.attach(MIMEText(config.send_registration_email.logo(), "html"))

    fp = open(config.send_registration_email.logo_path(),"rb")
    msgImg = MIMEImage(fp.read())
    fp.close()

    msgImg.add_header("Content-ID", "<image1>")
    msg.attach(msgImg)
    msg.attach(MIMEText(message, "html"))
    msg.attach(MIMEText(applicant_key,"html"))

    server = smtplib.SMTP(config.send_registration_email.server())
    server.starttls()
    server.login(msg["From"], password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
    return config.send_registration_email.response() + msg["To"]

router = APIRouter(prefix=settings.applicant_path)

@router.post("/")
async def request_registration(user: user.applicant_user):
    """Validate if the mail entered by the user is in the database, otherwise it calls the send_registratio_email function

    keywords arguments:
    user -- It is a parameter that inherits the properties of the applicant_user class 
    """
    if  users.find_one({'email': user.email}):
        raise HTTPException(status_code=404, detail="User already exists")
    else:
        return send_registration_email(user.email)

    
@router.get("/{hashed_email}")
async def read_email(hashed_email):
    item = {"detail": hashed_email}
    return item
    




