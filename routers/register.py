from fastapi import APIRouter

from dependencies import token_deps

from models.user import user_in, two_auth_in
from use_cases.user_cases import (
    save_user_in_db,
    activate_user,
    validate_qr_registration
    )


router_of_registry = APIRouter()


@router_of_registry.post("/save_user")
async def save_user(user: user_in) -> dict:
    """
        Validates user data by verifying if that the user doesn't exist in the
        database and creates the model to be added to the user collection

        Parameters
        ----------
        - **user**: pydantic class
            Class extending user_to_register, contains all the information
            about a user

        Returns
        ----------
        - **response**: dict
            Email sent to the user containing generated QR

        Raises
        ----------
        - **HTTPException**:
            If email is alredy registered
    
        - **ValueError**:
            If email is not valid

        - **ValueError**:
            If name has non-alphabetic values

        - **ValueError**:
            If last_name has non-alphabetic values

        - **ValueError**:
            If sex contains characters other than M or F

        - **ValueError**:
            If phone_number is not valid

        - **ValueError**:
            If the verified password doesn't match
    """
    return save_user_in_db(user)


@router_of_registry.post("/qr_validation")
async def qr_validation(user: two_auth_in) -> dict:
    """
        Validate the code given by Google Authenticator

        Parameters
        ----------
        - **user**: pydantic class
            Class extending two_auth_in, contains the data necessary for
            two factor authentication

        Returns
        ----------
        - **response**: str
            Send link with the tokenized information to user's email

        Raises
        ----------
        - **HTTPException**:
            If email isn't stored in the database
        - **HTTPException**:
            If email doesn't match the key_qr
        - **ValueError**:
            If email is not valid
    """
    return validate_qr_registration(user.email, user.qr_value)


@router_of_registry.get("/{token_email}")
async def read_email(token_email):
    """
        Read the tokenized email, check if it is inside the database
        and update user's status to active

        Parameters
        ----------
        - **token_email**: str
            String containing a tokenized version of the user's email

        Returns
        ----------
        - **response**: dict

        Raises
        ----------
        - **HTTPException**:
            If token or email key don't exist
        - **HTTPException**:
            If status update is not successful
        - **HTTPException**:
            If user's email cannot be found
    """
    untokenized_email = token_deps.validate_access_token_email(token_email)
    return activate_user(untokenized_email)
