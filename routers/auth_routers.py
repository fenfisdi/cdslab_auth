from fastapi import APIRouter
from models import user
from uses_cases.auth_cases import validation_login_auth, validation_qr_auth


router = APIRouter()

@router.post("/loginAuthentication")
async def login_auth(user: user.auth_in):
    """
    validates user login

    Parameters
    ----------
    - user: dict
            A string email
    Returns
    ----------
    - **response** : string
            key_qr
            email

    Raises
    ----------
    - **HTTPException**
            If the password not is equal
    - **HTTPException**
            If user not exist

    """
    is_login = validation_login_auth(user)
    return is_login


@router.post("/qrAuthentication")
async def qr_auth(user: user.two_auth_in):
    """
    validates the value of the qr with the value entered by the user
    and generate the token

    Parameters
    ----------
    - email: str
            A string email

    - qr_value: int
            A int user-typed value
    Returns
    ----------
    - **response** : string
            token

    Raises
    ----------
    - **HTTPException**
            If the token is invalid or the email key doesn´t exist
    - **HTTPException**
            If incorret key_qr value

    """

    is_auth = validation_qr_auth(user.email, user.qr_value)
    return is_auth
