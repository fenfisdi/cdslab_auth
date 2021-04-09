from datetime import datetime, timedelta

from fastapi import APIRouter, status

from src.interfaces.user_interface import UserInterface
from src.models.user import PreAuthenticatedUser, AuthenticatedUser, \
    RecoverUser, SecurityCode, user_email, enter_responses
from src.use_cases.qr_deps import validate_qr
from src.use_cases.token_deps import generate_token_jwt
from src.use_cases.user_deps import send_email, get_hash_password
from src.use_cases.user_deps import verify_password
from src.utils import LoginMessage, UserMessage
from src.utils.response import set_json_response
from src.utils.security_code import random_number_with_digits

authentication_routes = APIRouter()


@authentication_routes.post("/loginAuthentication", status_code=status.HTTP_200_OK)
async def login_auth(pre_authenticated_user: PreAuthenticatedUser):
    """
        Validate user information at login time

        Parameters
        ----------
        - pre_authenticated_user: dict
            email associated to the user

        Returns
        ----------
        - Method
            - key_qr: str
                Hash to match second authentication factor

            - email:str
                Email associated to the user

        Raises
        ----------
        - HTTPException
            If passwords don't match

        - HTTPException
            If user doesn't exist
    """
    retrieved_user = UserInterface.retrieve_user(
        email=pre_authenticated_user.email
    )

    if retrieved_user:
        is_equal = verify_password(pre_authenticated_user.password,
                                   retrieved_user["hashed_password"])
        if is_equal:
            data = {
                "key_qr": retrieved_user.get("key_qr"),
                "email": retrieved_user.get("email"),
            }
            return set_json_response(
                LoginMessage.logged,
                status.HTTP_200_OK,
                data
            )

        return set_json_response(
            LoginMessage.invalid_user,
            status.HTTP_404_NOT_FOUND
        )
    return set_json_response(
        UserMessage.not_found,
        status.HTTP_404_NOT_FOUND
    )


@authentication_routes.post("/qrAuthentication",
                            status_code=status.HTTP_200_OK)
async def qr_auth(authenticated_user: AuthenticatedUser):
    """
        Validate if qr and the user input match the 2FA and
        generates a token

        Parameters
        ----------
        - **email**: str
            User email

        - **qr_value**: int
            Code generated by Google Authenticator

        Returns
        ----------
        - **response**: str
            Token

        Raises
        ----------
        - **HTTPException**:
            If token is invalid or email doesn't exist

        - **HTTPException**:
            If key_qr does't match the expected value
    """
    is_valid = validate_qr(
        {"email": authenticated_user.email},
        authenticated_user.qr_value
    )

    if is_valid:
        retrieved_user = UserInterface.retrieve_user(
            email=authenticated_user.email)
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(retrieved_user["_id"]),
            "role": str(retrieved_user["role"]),
            "email": str(retrieved_user["email"]),
        }

        token = generate_token_jwt(payload)
        if token:
            return set_json_response(
                LoginMessage.logged,
                status.HTTP_200_OK,
                dict(token=token)
            )
        return set_json_response(
            LoginMessage.token_error,
            status.HTTP_404_NOT_FOUND
        )
    return set_json_response(
        LoginMessage.invalid_qr,
        status.HTTP_404_NOT_FOUND
    )


@authentication_routes.post("/refreshAuthentication")
async def refresh_auth(user: AuthenticatedUser):
    user_retrieve = UserInterface.retrieve_user(key_qr=user.qr_value)
    if user_retrieve:
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(user_retrieve["_id"]),
            "rol": str(user_retrieve["rol"]),
            "email": str(user_retrieve["email"]),
        }
        token = generate_token_jwt(payload)
        if token:
            return set_json_response(
                LoginMessage.logged,
                status.HTTP_200_OK,
                dict(token=token)
            )
        return set_json_response(
            LoginMessage.token_error,
            status.HTTP_404_NOT_FOUND
        )
    return set_json_response(
        LoginMessage.invalid_qr,
        status.HTTP_404_NOT_FOUND
    )


@authentication_routes.post("/securityCodeRecoverylink")
async def generate_security_code_link(user: RecoverUser):
    email = user.email

    searched_user = UserInterface.retrieve_user(email=email)
    if searched_user:
        security_code = random_number_with_digits(6)
        is_updated = UserInterface.update_user_state(
            {'security_code': security_code}, searched_user['_id'])
        if is_updated:
            send_email(
                user.email,
                'Recovery Message from settings',
                str(security_code))
            # TODO: return email?
            return set_json_response('email_sended', 200)
        return set_json_response('Someting went wrong', 404)
    return set_json_response("User doesn´t exist", 404)


@authentication_routes.post("/validateSecuritycode")
async def validate_security_code(user: SecurityCode):
    email = user.email

    searched_user = UserInterface.retrieve_user(email=email)
    if searched_user:
        if str(searched_user['security_code']) == str(user.security_code):
            # TODO: return email?
            return set_json_response('any_message', 200)
        return set_json_response('invalid code', 400)
    return set_json_response('user doesnt exist', 404)


@authentication_routes.post("/passwordRecover")
async def password_recover(user: RecoverUser):
    email = user.email

    searched_user = UserInterface.retrieve_user(email=email)
    if searched_user:
        is_updated = UserInterface.update_user_state({
            'hashed_password': get_hash_password(user.new_password)},
            searched_user['_id'])
        if is_updated:
            return set_json_response('Password Changed', 200)
        return set_json_response('Password can not be updated', 400)
    return set_json_response('user doesnt exist', 404)


@authentication_routes.post("/qrRecoveryvinculation")
async def qr_recovery_vinculation(user: user_email):
    email = user.email

    searched_user = UserInterface.retrieve_user(email=email)
    # TODO: Model didn't have answer
    if user.answers == searched_user['security_questions']['answers']:
        if "security_questions" in searched_user:
            # TODO: Return Question Security
            return set_json_response('Any_Message', 200, {'data': 'question'})
        return set_json_response('Dint Have Security Question', 404)
    return set_json_response('Invalid User', 400)


@authentication_routes.post("/validateAnswers")
async def validate_security_answers(user: enter_responses):
    email = user.email

    searched_user = UserInterface.retrieve_user(email=email)
    # TODO: Model didn't have answer
    if user.answers == searched_user['security_questions']['answers']:
        if "security_questions" in searched_user:
            # TODO: Return Question Security
            return set_json_response('Any_Message', 200, {'data': 'question'})
        return set_json_response('Dint Have Security Question', 404)
    return set_json_response('Invalid User', 400)
