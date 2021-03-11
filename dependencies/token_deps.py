from fastapi import HTTPException, status
from jose import jwt, JWTError
from dotenv import dotenv_values
from pydantic import EmailStr

from models import user

secrets = dotenv_values(".secrets")


def validate_access_token_email(token: str) -> user.user_to_register:
    """
    Decode de tokenized email and return a dict with key pair email: decode_email

    Parameters
    ----------
    token_email: str
        A string generated by the email_access_token function

    Returns
    ----------
    decode_email: class applicant_user
        The key pair whit the value of the email entered by the user in the post method
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access Denied"
    )
    try:
        decode_email = jwt.decode(
            token, secrets["SECRET_KEY"], algorithms=secrets["ALGORITHM"])
        if decode_email["email"] is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return decode_email


def generate_token_jwt(payload: dict):
    """
        generate token given a payload

        Parameters
        ----------
        payload: dict
            dictionary with values to tokenize

        Returns
        ----------
        token: str 
            token for route protection
    """
    token = jwt.encode(
        payload, secrets["SECRET_KEY"], algorithm=secrets["ALGORITHM"])

    return {
        "access_token": token
    }
