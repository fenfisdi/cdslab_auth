from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from dotenv import dotenv_values

from dependencies import user_deps, qr_deps, responses
from operations.user_operations import *

settings = dotenv_values(".env")


def save_user_in_db(user: dict) -> dict:

    if retrieve_user({'email': user.email}):
        return responses.error_response_model('User already exists', 404, 'Error')
    user_in_db = user_deps.transform_props_to_user(user)
    user_insert = insert_user(user_in_db.dict())
    if user_insert:
        url_path = qr_deps.generate_url_qr(user_in_db.key_qr, user)
        return responses.response_model(
            {
                'email': user_in_db.email,
                'urlPath': url_path,
                'keyQr': user_in_db.key_qr
            },
            "successful"
        )
    return responses.error_response_model('insert error in users collection', 404, 'Error')


def activate_user(user: dict) -> dict:

    is_user = retrieve_user({'email': user['email']})

    if is_user:
        is_updated = update_user_state({'is_active': True}, is_user['_id'])
        if is_updated:
            return RedirectResponse(settings["ALLOWED_ORIGINS"])
        return responses.error_response_model("error to activate account", 404, "Error")
    return responses.error_response_model("user not found", 404, "Error")


def validate_qr_registration(email: str, qr_value: str) -> str:

    is_validate = qr_deps.validate_qr({"email": email}, qr_value)
    if is_validate:
        user_deps.send_email(email)
        return "Check your email to finish the registration process"
    return responses.error_response_model("authorization failure", 404, "Error")
