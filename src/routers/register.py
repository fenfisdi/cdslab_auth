from fastapi import APIRouter
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from src.models import NewUser, OTPUser
from src.services import UserAPI
from src.use_cases import SecurityUseCase
from src.utils import UserMessage, LoginMessage
from src.utils.response import UJSONResponse

registry_routes = APIRouter(prefix='/register', tags=['Register'])


@registry_routes.post("/user", status_code=HTTP_201_CREATED)
def create_user(user: NewUser):
    """
    Validates user data by verifying if that the user doesn't exist in the
    database and creates the model to be added to the user collection.

    \f
    :param user: contains all the information about a user
    """
    data = user.dict(exclude={'verify_password'})
    data['otp_code'] = SecurityUseCase.create_otp_code()
    response, is_invalid = UserAPI.create_user(data)
    if is_invalid:
        return response

    user_found = response.get('data')
    user_found['otp_code'] = data.get('otp_code')
    user_found['url'] = SecurityUseCase.create_otp_url(
        user_found.get('otp_code'),
        user_found.get('email')
    )
    return UJSONResponse(UserMessage.created, HTTP_201_CREATED, user_found)


@registry_routes.post('/user/otp', status_code=HTTP_200_OK)
def validate_user_otp(user: OTPUser):
    """
    Validate the code given by Google Authenticator

    \f
    :param user: Contains the data necessary for two factor authentication.
    """
    response, is_invalid = UserAPI.find_user(user.email, True)
    if is_invalid:
        return response

    otp_code = SecurityUseCase.transform_otp_code(user.otp_code)

    response, is_invalid = UserAPI.find_otp_code(user.email)
    if is_invalid:
        return response

    data = response.get('data')
    auth_code = SecurityUseCase.transform_otp_code(data.get('otp_code'))
    if auth_code != otp_code:
        return UJSONResponse(LoginMessage.invalid_qr, HTTP_400_BAD_REQUEST)

    token = SecurityUseCase.encode_token_email(user.email)
    # TODO: Send Email
    return UJSONResponse(LoginMessage.validate_email, HTTP_200_OK)


@registry_routes.get('/user/email')
def validate_user_email(token: str):
    """
    Read the tokenized email, check if it is inside the database
    and update user's status to active.

    \f
    :param token: jwt token with the user information to validate.
    """
    data, is_valid = SecurityUseCase.decode_token(token)
    if not is_valid:
        return UJSONResponse(
            LoginMessage.invalid_token,
            HTTP_422_UNPROCESSABLE_ENTITY
        )

    email = data.get('email')

    response, is_valid = UserAPI.find_user(email, True)
    if is_valid:
        return response

    if response.get('data').get('email') != email:
        return UJSONResponse(UserMessage.not_found, HTTP_404_NOT_FOUND)

    response, is_valid = UserAPI.validate_user(email)
    if not is_valid:
        return response
    return UJSONResponse(UserMessage.verified, HTTP_200_OK)
