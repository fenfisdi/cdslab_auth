from dotenv import dotenv_values
from fastapi import HTTPException, status
from jose import jwt, JWTError

secrets = dotenv_values(".secrets")


def validate_email_access_token(token: str) -> str:
    """
        Extract email from token and return a key pair

        Parameters
        ----------
        token: str
            A string generated by the email_access_token function

        Returns
        ----------
        decode_email: class applicant_user
            Key pair for the associated email
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access Denied"
        )
    try:
        decoded_email = jwt.decode(token,
                                   secrets["SECRET_KEY"],
                                   algorithms=secrets["ALGORITHM"])
        if decoded_email["email"] is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return decoded_email['email']


def generate_token_jwt(payload: dict):
    """
        Generate token and respective payload

        Parameters
        ----------
        payload: dict
            Dictionary with values to tokenize

        Returns
        ----------
        token: str
            Token for route protection
    """
    token = jwt.encode(payload,
                       secrets["SECRET_KEY"],
                       algorithm=secrets["ALGORITHM"])
    return { "access_token": token }
