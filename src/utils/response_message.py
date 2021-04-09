from dataclasses import dataclass


@dataclass
class UserMessage:
    exist: str = "User already exist"
    not_found: str = "User not found"
    created: str = "User has been created"
    invalid: str = "Can not create user"
    verified: str = "User has been verified"
    not_valid: str = "User can not activate"


@dataclass
class LoginMessage:
    invalid_user: str = "Invalid Username or Password"
    invalid_qr: str = "Invalid QR code"
    invalid_token: str = "Invalid token"
    logged: str = "User logged in"
    token_error: str = "Can not create token"
    validate_email: str = "Check your email to finish the registration process"
