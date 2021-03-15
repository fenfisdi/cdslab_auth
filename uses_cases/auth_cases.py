from operations.user_operations import *
from models.user import *
from pprint import pprint
from dependencies import user_deps, responses, qr_deps, token_deps
from fastapi import HTTPException
import time
from bson.objectid import ObjectId
from datetime import datetime, timedelta


def validation_login_auth(data: auth_in):
    user_retrieve = retrieve_user({"email": data.email})
    if user_retrieve:
        pprint(user_retrieve)
        is_equal = user_deps.verify_passowrd(
            data.password, user_retrieve['hashed_password']
        )
        if is_equal:
            return responses.response_model({'key_qr': user_retrieve['key_qr'], 'email': user_retrieve['email']}, "successfull")

        raise HTTPException(
            status_code=404,
            detail=responses.error_response_model(
                'user or password invalid!', 404, 'Error'
            )
        )

    raise HTTPException(
        status_code=404, detail=responses.error_response_model(
            'user or password invalid!', 404, 'Error'
        )
    )


def validation_qr_auth(email: str, qr_value: str):

    is_validate = qr_deps.validate_qr({"email": email}, qr_value)
    if is_validate:
        user_retrieve = retrieve_user({"email": email})
        pprint(user_retrieve)
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(user_retrieve["_id"]),
            "email": str(user_retrieve["email"]),
        }

        token = token_deps.generate_token_jwt(payload)
        if token:
            return responses.response_model(token, "successfull")
        raise HTTPException(
            status_code=404,
            detail=responses.error_response_model(
                'error generating usaurio token', 404, 'Error'
            )
        )
    raise HTTPException(
        status_code=404,
        detail=responses.error_response_model(
            'incorrect credentials for qr validation', 404, 'Error'
        )
    )


def generate_refresh_token(key_qr):
    user_retrieve = retrieve_user({"key_qr": key_qr})
    if user_retrieve:
        pprint(user_retrieve)
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(user_retrieve["_id"]),
            "email": str(user_retrieve["email"]),
        }

        token = token_deps.generate_token_jwt(payload)
        if token:
            return responses.response_model(token, "successfull")
        raise HTTPException(
            status_code=404,
            detail=responses.error_response_model(
                'error generating usaurio token', 404, 'Error'
            )
        )
    raise HTTPException(
        status_code=404,
        detail=responses.error_response_model(
            'incorrect key', 404, 'Error'
        )
    )
