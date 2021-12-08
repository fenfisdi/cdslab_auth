from dataclasses import dataclass


@dataclass
class UserMessage:
    created: str = "User has been created"
    exist: str = "User already exist"
    invalid: str = "Can not create user"
    not_found: str = "User not found"
    not_valid: str = "User can not activate"
    verified: str = "User has been verified"
    found: str = "User Found"
    updated: str = "User Updated"


@dataclass
class LoginMessage:
    found_question: str = "Security Questions Found"
    invalid_answers: str = "Invalid Answers"
    invalid_code: str = "Invalid Security Code"
    invalid_qr: str = "Invalid OTP code"
    invalid_token: str = "Invalid token"
    invalid_user: str = "Invalid Username or Password"
    logged: str = "User logged in"
    success_code: str = "Success code"
    token_error: str = "Can not create token"
    validate_email: str = "Check your email to finish the registration process"


@dataclass
class SecurityMessage:
    invalid_user: str = 'Invalid User'
    invalid_token: str = "Invalid Token"
