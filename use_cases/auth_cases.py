import random
import time
import jsoncfg

from fastapi import HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from pprint import pprint

from dependencies import user_deps, responses, qr_deps, token_deps, common
from models.user import *
from operations.user_operations import retrieve_user, update_user_state


def validation_login_auth(data: auth_in):
    user_retrieve = retrieve_user({"email": data.email})
    if user_retrieve:
        if user_retrieve['is_active']:
            is_equal = user_deps.verify_passoword(
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


def send_security_code(user: dict) -> dict:

    searched_user = retrieve_user({'email': user.email})
    if searched_user:
        security_code = common.random_number_with_digits(6)
        is_updated = update_user_state(
            {'security_code': security_code}, searched_user['_id'])
        if is_updated:            
            user_deps.send_email(
                user.email, 
                send_registration_email.message.recovery_password(), 
                str(security_code))
            return responses.response_model({'email': user.email}, "email sended")
        return responses.error_response_model('Someting went wrong', 404, "Error")
    return responses.error_response_model("User doesn´t exist", 404, "Error")


def validate_securtity_code(user: dict) -> dict:

    searched_user = retrieve_user({'email': user.email})
    if searched_user:
        if str(searched_user['security_code']) == str(user.security_code):
            return responses.response_model({'email': user.email}, "true")
        return responses.error_response_model("Invalid code", 404, "Error")
    return responses.error_response_model('User doesn´t exist', 404, "Error")


def update_password(user: dict) -> dict:

    searched_user = retrieve_user({'email': user.email})
    if searched_user:
        is_updated = update_user_state({
            'hashed_password': user_deps.get_hash_password(user.new_password)},
            searched_user['_id'])
        if is_updated:
            return responses.response_model({'passwordChanged':True}, 
            "password updated")
        return responses.error_response_model("Password can´t be updated", 
        404, "Error")
    return responses.error_response_model("User not found", 404, "Error")


def retrieve_security_questions(user: dict) -> dict:

    searched_user = retrieve_user({"email": user.email})
    if searched_user:
        if "security_questions" in searched_user:
            return responses.response_model(
                {"securityQuestions": searched_user["security_questions"]["questions"],
                'email': searched_user['email']},
                "success")
        return responses.error_response_model("User has no security questions", 404, "Error")
    return responses.error_response_model("Invalid user", 404, "user doesn´t exists")


def validate_security_questions(user: dict) -> dict:

    searched_user = retrieve_user({'email': user.email})
    if searched_user:
        if user.answers == searched_user['security_questions']['answers']:
            url_path = qr_deps.generate_url_qr(searched_user['key_qr'], user)
            return responses.response_model(
                {'email': searched_user['email'],
                'urlPath': url_path,
                'keyQr': searched_user['key_qr']},
                "successful"
            )
        return responses.error_response_model("Invalid answers. please try again", 404, "Error")
    return responses.error_response_model("User doesn't exist", 404, "Error")
