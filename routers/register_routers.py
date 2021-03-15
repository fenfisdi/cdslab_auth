from fastapi import APIRouter

from uses_cases.user_cases import *
from models import user
from dependencies import token_deps


router = APIRouter()

@router.post("/save_user")
async def save_user(user: user.user_in) -> dict:
    """
    Validates the data entered by the user, confirms that the user 
    does not exist within the database and creates the model that will 
    be saved in the user collection 

    Parameters
    ----------
    - **user** : pydantic class 
            It's a parameter that inherits the properties of the user_to_register class

    Returns
    ----------
    - **response** : dict 
            Sended the email to the user and returns the url QR generated

    Raises
    ----------
    - **HTTPException**
        If the email is registered in the database
    - **ValueError**
        If the email is not a valid email address
    - **ValueError**
        If the name is not alphabetic
    - **ValueError**
        If the last_name is not alphabetic
    - **ValueError**
        If the sex is not M or F
    - **ValueError**
        If the phone_number is not a valid phone number
    - **ValueError**
        If the password and verify password doesn't match
    """
    response = save_user_in_db(user)

    return response

@router.post("/qr_validation")
async def qr_validation(user: user.two_auth_in) -> dict:

    response = validate_qr_registration(user.email, user.qr_value)
    return response


@router.get("/{token_email}")
async def read_email(token_email):
    """
    Decode de tokenized email, check if the email is in the database 
    and change the status of is_active to true

    Parameters
    ----------
    - **token_email**: str
            A string generated by the email_access_token function

    Returns
    ----------
    - **response** : dict
            response generated by the responses file
    
    Raises
    ----------
    - **HTTPException**
            If the token is invalid or the email key doesn´t exist
    - **HTTPException**
            If the update is not success
    - **HTTPException**
            If the update is not success   
    - **HTTPException**
            If the user email search is not success 
    """
    untokenized_email = token_deps.validate_access_token_email(token_email)
    response = activate_user(untokenized_email)

    return response




