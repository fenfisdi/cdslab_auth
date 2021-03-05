import json

from fastapi import HTTPException, APIRouter
from jose import JWTError, jwt
from dotenv import dotenv_values

from db_connection import users
from models import user

settings = dotenv_values(".env")
secrets = dotenv_values(".secrets")

router = APIRouter(prefix=settings["APPLICANT_PATH"])


@router.post("/")
async def request_registration(user: user.applicant_user):
    """Validate if the mail entered by the user is in the database, 
     otherwise it calls the send_registratio_email function


    Parameters
    ----------
    user : pydantic class 
            It is a parameter that inherits the properties of the applicant_user class

    Returns
    ----------
    str
        Sended the email to the user and return the confirmations that the email was sended

    Raises
    ----------
    HTTPException
        If the email is registered in the database
    ValueError
        If the email is not a valid email address
    """
    if  users.find_one({'email': user.email}):
        raise HTTPException(status_code=404, detail="User already exists")
    else:
        return user.send_registration_email(user.email)


@router.get("/{token_email}")
async def read_email(token_email):
    """Decode de tokenized email and return a dict with key pair email: decode_email

    Parameters
    ----------
    token_email: str
        A string generated by the email_access_token function

    Returns
    ----------
    decode_email: class applicant_user
        The key pair whit the value of the email entered by the user in the post method
    """
    decode_email = jwt.decode(token_email, secrets["SECRET_KEY"], algorithms=secrets["ALGORITHM"])

    return decode_email





