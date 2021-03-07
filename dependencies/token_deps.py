from fastapi import HTTPException, status
from jose import jwt, JWTError
from dotenv import dotenv_values

from models import user

secrets = dotenv_values(".secrets")

def validate_access_token_email(token: str) -> user.applicant_user:
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
        detail="Access Denied",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decode_email = jwt.decode(token, secrets["SECRET_KEY"], algorithms=secrets["ALGORITHM"])
        if decode_email["email"] is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return decode_email
