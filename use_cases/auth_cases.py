import time
import jsoncfg

from fastapi import HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from pprint import pprint

from dependencies import user_deps, responses, qr_deps, token_deps
from models.user import *
from operations.user_operations import retrieve_user


def validation_login_auth(data: auth_in):
    user_retrieve = retrieve_user({"email": data.email})
    if user_retrieve:
        if user_retrieve['is_active']:
            is_equal = user_deps.verify_passowrd(
                data.password, user_retrieve['hashed_password']
            )
            if is_equal:
                return responses.response_model({'keyQr': user_retrieve['key_qr'],
                                                'email': user_retrieve['email']},
                                                'successful'
                                                )
            return responses.error_response_model('user not exist.', 404, 'Error')
        return responses.error_response_model('Inactive user', 404, 'Error')
    return responses.error_response_model('user not exist.', 404, 'Error')


def validation_qr_auth(email: str, qr_value: str):

    is_validate = qr_deps.validate_qr({"email": email}, qr_value)
    if is_validate:
        user_retrieve = retrieve_user({"email": email})
        pprint(user_retrieve)
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(user_retrieve["_id"]),
            "rol": str(user_retrieve["rol"]),
            "email": str(user_retrieve["email"]),
        }

        token = token_deps.generate_token_jwt(payload)
        if token:
            return responses.response_model(token, "successfull")
        return responses.error_response_model('error generate token', 404, 'Error')
    return responses.error_response_model('incorret valition qr credentials', 404, 'Error')


def generate_refresh_token(key_qr):
    user_retrieve = retrieve_user({"key_qr": key_qr})
    if user_retrieve:
        pprint(user_retrieve)
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(user_retrieve["_id"]),
            "rol": str(user_retrieve["rol"]),
            "email": str(user_retrieve["email"]),
        }

        token = token_deps.generate_token_jwt(payload)
        if token:
            return responses.response_model(token, "successfull")
        return responses.error_response_model('Error generating user token', 404, 'Error')
    return responses.error_response_model('Incorrect key', 404, 'Error')


def send_recovery_link_password(user: dict) -> dict:

    if retrieve_user({'email': user.email}):
        user_deps.send_email(
            user.email, settings['AUTHENTICATION_PATH'], send_registration_email.message.recovery_password())
        return responses.response_model({}, "email sended")
    return responses.error_response_model('User doesn´t exist', 404, "Error")


def update_password(user: dict) -> dict:

    is_user = retrieve_user({'email': user.email})

    if is_user:
        is_updated = update_user_state({'hashed_password': user_deps.get_hash_password(
            user.new_password)}, is_user['_id'])
        if is_updated:
            return responses.response_model({user.new_password}, "password updated")
        return responses.error_response_model("password can´t be updated", 404, "Error")
    return responses.error_response_model("user not found", 404, "Error")


def retrieve_security_questions(user: dict) -> dict:

    is_user = retrieve_user({'email': user.email})

    if is_user:
        security_questions = {
            'security_questions': is_user['security_questions']['questions']}
        if security_questions:
            return responses.response_model(security_questions, "success")
        return responses.error_response_model("Invalid operation", 404, "Error")
    return responses.error_response_model("Invalid user", 404, "user doesn´t exists")


def validate_security_questions(user: dict) -> dict:

    is_user = retrieve_user({'email': user.email})

    if is_user:
        security_answers = {
            'answers': is_user['security_questions']['answers']
        }
        if user.answers == security_answers['answers']:
            url_path = qr_deps.generate_url_qr(is_user['key_qr'], user)
            return responses.response_model({
                'email': is_user['email'],
                'urlPath': url_path,
                'keyQr': is_user['key_qr']
            },
                "successful"
            )
        return responses.error_response_model("authentication error", 404, "please try again")
    return responses.error_response_model("user doesn't exist", 404, "Error")
