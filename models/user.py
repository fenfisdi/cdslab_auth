import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from passlib.context import CryptContext
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError, validator
from jose import jws, JWSError

import secrets
import settings

from config import config

#shared properties
class applicant_user(BaseModel):
    
    email: EmailStr

    @classmethod
    def tokenize_email(cls, email):
        """Tokenize the email taken the applicant_user class as a parameter

        Parameters
        ----------
        email : str 
                the value of email entered by the user

        Returns
        ----------
        str
            The email tokenized by jws method
        """
        email_to_encode = {'email': email}
        tokenized_email = jws.sign(email_to_encode, secrets.secret_key, algorithm=secrets.algorithm)
        return tokenized_email 

    @classmethod
    def send_registration_email(cls, email):
        """Send registration email to the adress entered by the user


        Build the path that will be sent to the user and add the tokenized email, 
        then use the MIMEMultipart library to pack the welcome message, 
        the image and the link to the registration, finally it connects with 
        the google server and with the credentials of the specified email send the message


        Parameters
        ----------
        email : str 
                the value of email field in the applicant_user class

        Returns
        ----------
        str
            The confirmation with the email is sended

        """
        domain = settings.domain
        key_email = applicant_user.tokenize_email(email)
        key_email = f'{"/"}{key_email}'
        applicant_key = f'{domain}{settings.applicant_path}{key_email}'
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
        
class user_to_register(applicant_user):
    name: str = None
    last_name: str = None
    sex: str = None
    phone_numbre: str = None
    institution: str = None
    institution_afiliation: str = None
    profession: str = None
    date_of_birth: str = None
    is_active: Optional[bool] = True
    password: Optional[str] = None
    verify_password: Optional[str] = None

    @validator('verify_password')
    def password_match(cls, password_to_verify, values, **kwargs):
        """ Validate that the value taken by password and verify_password match

        Parameters
        ----------
        cls
            takes user_to_register class as an argument
        password_to_verify: str 
            is the value in the verify_password field 
        values: str
            is the value in the password field, by default the decorator takes 
            this name as a parameter
        **kwargs:  
            if provided, this will include the arguments above not explicitly 
            listed in the signature, this is necessary for the function takes 
            the key value pairs defined in the class

        Return:
        ----------
        password_to_verify: str
            If the password and verify_password match, returns the value in passowrd filed
        
        Raises:
        ----------
        ValueError
            If the password and verify_passowrd does'nt match

        """
        if 'password' in values and password_to_verify != values['password']:
            raise ValueError('passwords do not match')
        return password_to_verify
    


 