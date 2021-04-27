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
            invalid: bool = False
    ) -> Tuple[Optional[UJSONResponse], bool]:
        """
        Validate OTP code from user,

        :param email:
        :param otp_code:
        :param invalid:
        :return:
        """
        response, is_invalid = UserAPI.find_user(email, invalid)
        if is_invalid:
            return response, True

        response, is_invalid = UserAPI.find_otp_key(email)
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
