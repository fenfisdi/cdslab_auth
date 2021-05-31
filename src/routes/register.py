from fastapi import APIRouter
from starlette.background import BackgroundTasks
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from src.models import NewUser, OTPUser
from src.services import UserAPI
from src.use_cases import SendEmailVerificationUseCase, ValidateOTPUseCase
from src.utils.messages import LoginMessage, UserMessage
from src.utils.response import UJSONResponse
from src.utils.security import Security

registry_routes = APIRouter(prefix='/register', tags=['Register'])


@registry_routes.post("/user", status_code=HTTP_201_CREATED)
def create_user(user: NewUser):
    """
    Validates user data by verifying if that the user doesn't exist in the
    database and creates the model to be added to the user collection.

    \f
    :param user: contains all the information about a user
    """
    data = user.dict()
    data['otp_code'] = Security.create_otp_key()
    response, is_invalid = UserAPI.create_user(data)
    if is_invalid:
        return response

    user_found = response.get('data')
    user_found['otp_code'] = data.get('otp_code')
    user_found['url'] = Security.create_otp_url(
        user_found.get('otp_code'),
        user_found.get('email')
    )
    return UJSONResponse(UserMessage.created, HTTP_201_CREATED, user_found)


@registry_routes.post('/user/otp', status_code=HTTP_200_OK)
def validate_user_otp(user: OTPUser, background_tasks: BackgroundTasks):
    """
    Validate the code given by OTP application

    \f
    :param background_tasks:
    :param user: Contains the data necessary for two factor authentication.
    """
    response, is_invalid = ValidateOTPUseCase.handle(
        user.email,
        user.otp_code,
        is_valid=False
    )
    is_invalid = False
    if is_invalid:
        return response

    token = Security.encode_token(dict(email=user.email))

    # TODO: Create Magic URL
    data = {
        'email': user.email,
        'subject': 'Verification Mail',
        'message': 'Your Verification mail is',
    }

    background_tasks.add_task(
        SendEmailVerificationUseCase.handle,
        user.email,
        token
    )

    return UJSONResponse(LoginMessage.validate_email, HTTP_200_OK)


@registry_routes.get('/user/email')
def validate_user_email(token: str):
    """
    Read the tokenized email, check if it is inside the database
    and update user's status to active.

    \f
    :param token: jwt token with the user information to validate.
    """
    data, is_valid = Security.decode_token(token)
    if not is_valid:
        return UJSONResponse(
            LoginMessage.invalid_token,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    email = data.get('email')

    response, is_valid = UserAPI.find_user(email, False)
    if is_valid:
        return response

    if response.get('data').get('email') != email:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    response, is_valid = UserAPI.validate_user(email)
    if not is_valid:
        return response
    return UJSONResponse(UserMessage.verified, HTTP_200_OK)
