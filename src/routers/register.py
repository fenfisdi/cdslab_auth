from fastapi import APIRouter, status

from src.interfaces.user_interface import UserInterface
from src.models.user import User, AuthenticatedUser
from src.use_cases.qr_deps import generate_url_qr, validate_qr
from src.use_cases.token_deps import validate_email_access_token
from src.use_cases.user_deps import send_email, transform_props_to_user
from src.utils import UserMessage, LoginMessage
from src.utils.response import set_json_response

router_of_registry = APIRouter()


@router_of_registry.post("/save_user", status_code=status.HTTP_201_CREATED)
async def save_user(user: User):
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
        return set_json_response(UserMessage.exist, status.HTTP_400_BAD_REQUEST)

    else:
        #TODO: RENAME ME, PLS
        user_in_db = transform_props_to_user(user)
        inserted_user = UserInterface.insert_user(user_in_db.dict())

        if inserted_user:
            url_path = generate_url_qr(user_in_db.key_qr, user)
            data = {
                'email': user_in_db.email,
                'url_path': url_path,
                'key_qr': user_in_db.key_qr
            }
            return set_json_response(UserMessage.created, status.HTTP_201_CREATED, data)
        else:
            return set_json_response(UserMessage.invalid, status.HTTP_422_UNPROCESSABLE_ENTITY)


@router_of_registry.post("/qr_validation", status_code=status.HTTP_200_OK)
async def qr_validation(authenticated_user: AuthenticatedUser):
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
        return set_json_response(LoginMessage.validate_email, status.HTTP_400_BAD_REQUEST)
    return set_json_response(LoginMessage.invalid_qr, status.HTTP_404_NOT_FOUND)


@router_of_registry.get("/{tokenized_email}", status_code=status.HTTP_200_OK)
async def read_email(tokenized_email):
    """
        Read the tokenized email, check if it is inside the database
        and update user's status to active

        Parameters
        ----------
        - **tokenized_email**: str
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
    is_valid, email = validate_email_access_token(tokenized_email)
    if not is_valid:
        return set_json_response(LoginMessage.invalid_token, status.HTTP_422_UNPROCESSABLE_ENTITY)

    user_email = UserInterface.retrieve_user(email=email)

    if user_email:
        is_updated = UserInterface.update_user_state({'is_active': True}, user_email['_id'])
        if is_updated:
            return set_json_response(UserMessage.verified, status.HTTP_200_OK, is_updated)
        return set_json_response("error to activate account", status.HTTP_404_NOT_FOUND)
    return set_json_response("user not found", status.HTTP_404_NOT_FOUND)
