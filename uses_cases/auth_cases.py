from operations.user_operations import *
from models.user import *
from pprint import pprint
from dependencies import user_deps, responses, qr_deps, token_deps
from fastapi import HTTPException
import time
from bson.objectid import ObjectId
from datetime import datetime, timedelta


def validation_login_auth(data: auth_in):
    user_retrive = retrive_user({"email": data.email})
    if user_retrive:
        pprint(user_retrive)
        is_equal = user_deps.verify_passowrd(
            data.password, user_retrive['hashed_password'])
        if is_equal:
            return responses.response_model({'key_qr': user_retrive['key_qr'], 'email': user_retrive['email']}, "successfull")

        return responses.error_response_model('password not is equal', 404, 'Error')

    return responses.error_response_model('user not exist.!', 404, 'Error')


def validation_qr_auth(email: str, qr_value: str):

    is_validate = qr_deps.validate_qr({"email": email}, qr_value)
    if is_validate:
        user_retrive = retrive_user({"email": email})
        pprint(user_retrive)
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(user_retrive["_id"]),
            "rol": str(user_retrive["rol"]),
            "email": str(user_retrive["email"]),
        }

        token = token_deps.generate_token_jwt(payload)
        if token:
            return responses.response_model(token, "successfull")
        return responses.error_response_model('error generate token', 404, 'Error')
    return responses.error_response_model('incorret valition qr credentials', 404, 'Error')
