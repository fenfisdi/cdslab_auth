import time

from fastapi import HTTPException
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from pprint import pprint

from dependencies import user_deps, responses, qr_deps, token_deps
from models.user import *
from operations.user_operations import *


def validation_login_auth(data: auth_in):
    user_retrieve = retrieve_user({"email": data.email})
    if user_retrieve:
        if user_retrieve['is_active']:
            is_equal = user_deps.verify_passowrd(
                data.password, user_retrieve['hashed_password']
            )
            if is_equal:
                return responses.response_model({'key_qr': user_retrieve['key_qr'],
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
