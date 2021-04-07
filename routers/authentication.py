import pyotp

from fastapi import APIRouter
from pprint import pprint

from dependencies import token_deps
from models import user
from use_cases.auth_cases import (validation_login_auth,
                                  validation_qr_auth,
                                  generate_refresh_token,
                                  send_security_code,
                                  validate_securtity_code,
                                  update_password,
                                  retrieve_security_questions,
                                  validate_security_questions
                                  )

router_of_authentication = APIRouter()


@router_of_authentication.post("/loginAuthentication")
async def login_auth(user: user.auth_in):
    """
        Validate user information at login time

        Parameters
        ----------
        - user: dict
            email associated to the user

        Returns
        ----------
        - response : Method
            - key_qr: str
                Hash to match second authentication factor
            - email:str
                Email associated to the user

        Raises
        ----------
        - HTTPException
            If passwords don't match
        - HTTPException
            If user doesn't exist
    """
    return validation_login_auth(user)


@router_of_authentication.post("/qrAuthentication")
async def qr_auth(user: user.two_auth_in):
    """
        Validate if qr and the user input match the authentication factor and
        generates a token

        Parameters
        ----------
        - **email**: str
            User email

        - **qr_value**: int
            Code generated by Google Authenticator

        Returns
        ----------
        - **response**: str
            Token

        Raises
        ----------
        - **HTTPException**:
            If token is invalid or email doesn't exist
        - **HTTPException**:
            If key_qr does't match the expected value
    """
    return validation_qr_auth(user.email, user.qr_value)


@router_of_authentication.post("/refreshAuthentication")
async def refresh_auth(user: user.auth_refresh):
    """
         Generate a new token to keep the user logged in

         Parameters
         ----------
         - **email**: str
            User email

         - **key_qr**: str
             String stored in the database

         Returns
         ----------
         - **response**: str
             token

         Raises
         ----------
         - **HTTPException**:
             If the token cannot be generated
         - **HTTPException**:
             If key_qr doesn't match the expected value
     """
    return generate_refresh_token(user.key_qr)


@router_of_authentication.post("/securityCodeRecoverylink")
async def generate_security_code_link(user: user.user_email):

    return send_security_code(user)


@router_of_authentication.post("/validateSecuritycode")
async def validate_security_code(user: user.security_code):

    return validate_securtity_code(user)


@router_of_authentication.post("/passwordRecover")
async def password_recover(user: user.recover_password):

    return update_password(user)


@router_of_authentication.post("/qrRecoveryvinculation")
async def qr_recovery_vinculation(user: user.user_email):

    return retrieve_security_questions(user)


@router_of_authentication.post("/validateAnswers")
async def validate_security_answers(user: user.enter_responses):

    return validate_security_questions(user)
