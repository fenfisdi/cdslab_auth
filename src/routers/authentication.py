from typing import List

from fastapi import APIRouter, status
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)

from src.models import (
    LoginUser,
    OTPUser,
    RecoverUser,
    SecurityCode,
    SecurityQuestion
)
from src.services import UserAPI
from src.use_cases import SecurityUseCase
from src.utils import LoginMessage
from src.utils.response import UJSONResponse
from src.utils.security import random_number_with_digits

authentication_routes = APIRouter(tags=["Authentication"])


@authentication_routes.post("/login", status_code=status.HTTP_200_OK)
def login_auth(user: LoginUser):
    """
    Validate user credentials and return ok if email and password match.

    \f
    :param user: user credentials as email and password.
    """
    response, is_invalid = UserAPI.validate_credentials(user.dict())
    if is_invalid:
        return response

    data = response.get('data')
    data['email'] = user.email

    return UJSONResponse(LoginMessage.logged, HTTP_200_OK, data)


@authentication_routes.post("/login/otp", status_code=status.HTTP_200_OK)
def login_otp_auth(user: OTPUser):
    """
    Validate if qr and the user input match the 2FA and generates a token.

    \f
    :param user: user credentials as email and password.
    """
    response, is_invalid = UserAPI.find_user(user.email)
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

    data = {
        'token': SecurityUseCase.encode_token_access(dict(email=user.email))
    }
    return UJSONResponse(LoginMessage.logged, HTTP_200_OK, data)


@authentication_routes.post('/login/recovery_code')
def create_security_code(email: str):
    """
    Create security code to specific user.

    \f
    :param email: user email to create security code.
    """
    response, is_invalid = UserAPI.find_user(email, False)
    if is_invalid:
        return response

    security_code = random_number_with_digits(6)
    response, is_invalid = UserAPI.save_security_code(email, security_code)
    if is_invalid:
        return response

    # TODO: Send Email


@authentication_routes.post('/login/validate_code')
def validate_security_code(user: SecurityCode):
    """
    Check if the security code is the user valid code, otherwise return not
    valid code.

    \f
    :param user: user information as email and security code.
    """
    response, is_invalid = UserAPI.find_user(user.email, False)
    if is_invalid:
        return response

    response, is_invalid = UserAPI.find_security_code(user.email)
    if is_invalid:
        return response

    if user.security_code == response.get('data').get('security_code'):
        return UJSONResponse(LoginMessage.success_code, HTTP_200_OK)
    return UJSONResponse(LoginMessage.invalid_code, HTTP_400_BAD_REQUEST)


@authentication_routes.post('/login/recover_password')
def recover_password(user: RecoverUser):
    """
    Update passwords from the user, verify if both passwords match update
    password user.

    \f
    :param user: user email and passwords to update.
    """
    response, is_invalid = UserAPI.find_user(user.email)
    if is_invalid:
        return response

    response, is_invalid = UserAPI.update_password(
        user.dict(exclude={'verify_password'})
    )
    if is_invalid:
        return response

    return UJSONResponse('updated', HTTP_200_OK)


@authentication_routes.get('/login/security_question')
def find_security_questions(email: str):
    """
    Find and return security questions from a specific user.

    \f
    :param email: user email to find security questions.
    """
    response, is_invalid = UserAPI.find_user(email)
    if is_invalid:
        return response

    response, is_invalid = UserAPI.find_security_questions(email)
    if is_invalid:
        return response

    data = response.get('data')

    return UJSONResponse(LoginMessage.found_question, HTTP_200_OK, data)


@authentication_routes.post('/login/security_questions')
def recover_otp(
        email: str,
        security_questions: List[SecurityQuestion]
):
    """
    Validate security questions from the user, if the validations is ok, will
    return email and new url to get otp code.

    \f
    :param email: user email to recover otp code.
    :param security_questions: list of security questions to validate.
    """
    response, is_invalid = UserAPI.find_user(email)
    if is_invalid:
        return response

    response, is_invalid = UserAPI.find_security_questions(email)
    if is_invalid:
        return response

    questions = response.get('data')
    valid = list()
    for question in security_questions:
        valid_question = next((
            in_question for in_question in questions
            if in_question.get('question') == question.question
        ), None)
        if valid_question is None:
            valid.append(False)
            continue
        if valid_question.get('answer') == question.answer:
            valid.append(True)
        else:
            valid.append(False)

    if not all(valid):
        return UJSONResponse(LoginMessage.invalid_answers, HTTP_400_BAD_REQUEST)

    response, is_invalid = UserAPI.find_otp_code(email)
    if is_invalid:
        return response
    data = response.get('data')
    data['email'] = email
    data['url'] = SecurityUseCase.create_otp_url(data.get('otp_code'), email)
    return UJSONResponse('any', HTTP_200_OK, data)
