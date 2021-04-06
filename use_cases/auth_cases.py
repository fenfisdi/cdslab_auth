from datetime import datetime, timedelta

from models.user import PreAuthenticatedUser
from operations.user_operations import retrieve_user
from dependencies.responses import response_model, error_response_model
from dependencies.token_deps import generate_token_jwt
from dependencies.user_deps import verify_passowrd
from dependencies.qr_deps import validate_qr


def validate_user_login(pre_authenticated_user: PreAuthenticatedUser):

    retrieved_user = retrieve_user({"email": pre_authenticated_user.email})
    if retrieved_user:
        is_equal = verify_passowrd(pre_authenticated_user.password,
                                   retrieved_user["hashed_password"])
        if is_equal:
            return response_model({"key_qr": retrieved_user["key_qr"],
                                   "email": retrieved_user["email"]},
                                   "Successful")

        return error_response_model("Invalid Username or Password", 404, "Error")
    return error_response_model("User doesn't exist", 404, "Error")


def validate_user_qr(email: str, qr_value: str):

    is_validate = validate_qr({"email": email}, qr_value)
    if is_validate:
        retrieved_user = retrieve_user({"email": email})
        payload = {
            "expires": str(datetime.utcnow() + timedelta(hours=24)),
            "id": str(retrieved_user["_id"]),
            "role": str(retrieved_user["role"]),
            "email": str(retrieved_user["email"]),
        }

        token = generate_token_jwt(payload)
        if token:
            return response_model(token, "Successful")
        return error_response_model("Error while generating token", 404, "Error")
    return error_response_model("Invalid QR validation", 404, "Error")
