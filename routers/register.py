from fastapi import APIRouter, status

from dependencies.qr_deps import generate_url_qr, validate_qr
from dependencies.responses import error_response_model, response_model
from dependencies.token_deps import validate_email_access_token
from dependencies.user_deps import send_email, transform_props_to_user
from models.user import User, AuthenticatedUser
from interfaces.user_interface import UserInterface

router_of_registry = APIRouter()


@router_of_registry.post("/save_user", status_code=status.HTTP_201_CREATED)
async def save_user(user: User) -> dict:
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
        #TODO
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
    if UserInterface.retrieve_user(email=user.email):
        return error_response_model('User already exists', 409, 'Error')

    else:
        #TODO: RENAME ME, PLS
        user_in_db = transform_props_to_user(user)
        inserted_user = UserInterface.insert_user(user_in_db.dict())

        if inserted_user:
            url_path = generate_url_qr(user_in_db.key_qr, user)
            return { 'email':user_in_db.email,
                     'url_path': url_path,
                     'key_qr': user_in_db.key_qr }
        else:
            return error_response_model(
                    'Error while creating user',
                    500,
                    'Error'
                    )


@router_of_registry.post("/qr_validation")
async def qr_validation(authenticated_user: AuthenticatedUser) -> dict:
    """
        Validate the code given by Google Authenticator

        Parameters
        ----------
        - **user**: pydantic class
            Class extending AuthenticatedUser, contains the data necessary for
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
    is_validate = validate_qr({"email": authenticated_user.email}, authenticated_user.qr_value)

    if is_validate:
        send_email(authenticated_user.email)
        # TODO: Check Data Response
        return "Check your email to finish the registration process"
    return error_response_model("authorization failure", 404, "Error")


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
    untokenized_email = validate_email_access_token(token_email)

    user_email = UserInterface.retrieve_user(email=untokenized_email)

    if user_email:
        is_updated = UserInterface.update_user_state({'is_active': True}, user_email['_id'])
        if is_updated:
            return response_model({'data': is_updated}, "successful")
        return error_response_model("error to activate account", 404, "Error")
    return error_response_model("user not found", 404, "Error")
