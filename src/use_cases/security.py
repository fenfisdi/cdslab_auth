from typing import Tuple, Optional

from pyotp import TOTP
from starlette.status import HTTP_400_BAD_REQUEST

from src.services import UserAPI
from src.utils.messages import LoginMessage
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
