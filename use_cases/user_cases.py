from fastapi import HTTPException

from dependencies import user_deps, qr_deps, responses
from operations.user_operations import *


def activate_user(user: dict) -> dict:

    is_user = retrieve_user({'email': user['email']})

    if is_user:
        is_updated = update_user_state({'is_active': True}, is_user['_id'])
        if is_updated:
            return responses.response_model(is_updated, "successful")
        return responses.error_response_model("error to activate account", 404, "Error")
    return responses.error_response_model("user not found", 404, "Error")

def validate_qr_registration(email: str, qr_value: str) -> str:

    is_validate = qr_deps.validate_qr({"email": email}, qr_value)
    if is_validate:
        user_deps.send_email(email)
        return "Check your email to finish the registration process"
    return responses.error_response_model("authorization failure", 404, "Error")
