from os import environ
from typing import Optional, Tuple

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pyotp import TOTP
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.services import UserAPI
from src.utils.messages import LoginMessage, SecurityMessage
from src.utils.response import UJSONResponse


class ValidateOTPUseCase:

    @classmethod
    def handle(
        cls,
        email: str,
        otp_code: str,
        is_valid: bool = False
    ) -> Tuple[Optional[UJSONResponse], bool]:
        """
        Validate OTP code from user in any state (valid, invalid) and return
        response if had any error in the request, else return a false.

        :param email: user email to validate otp code.
        :param otp_code: otp code to validate with otp key.
        :param is_valid: find user if have valid or invalid state.
        """
        response, is_invalid = UserAPI.find_user(email, is_valid)
        if is_invalid:
            return response, True

        response, is_invalid = UserAPI.find_otp_key(email, is_valid)
        if is_invalid:
            return response, True

        data = response.get('data')
        auth = TOTP(data.get('otp_code'))
        if not auth.verify(otp_code):
            return UJSONResponse(
                LoginMessage.invalid_qr,
                HTTP_400_BAD_REQUEST
            ), True

        return None, False


class SecurityUseCase:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

    @classmethod
    def validate(cls, token: str = Depends(oauth2_scheme)) -> dict:
        token_data = cls._validate_token(token)
        email = token_data.get('email')

        response, is_invalid = UserAPI.find_user(email, is_valid=True)
        if not is_invalid:
            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                SecurityMessage.invalid_user
            )

        data = response.get('data')
        user = dict(
            name=data.get('name'),
            email=data.get('email'),
            is_enabled=data.get('is_enabled')
        )

        return user

    @classmethod
    def _validate_token(cls, token: str) -> Optional[dict]:
        try:
            data = jwt.decode(
                token,
                environ.get('SECRET_KEY'),
                environ.get('ALGORITHM')
            )
            if not data.get('email'):
                raise HTTPException(
                    HTTP_401_UNAUTHORIZED,
                    SecurityMessage.invalid_token
                )
            return data
        except JWTError as error:
            raise HTTPException(HTTP_401_UNAUTHORIZED, str(error))
