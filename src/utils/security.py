from hashlib import sha256
from os import environ
from random import randint
from typing import Union, Tuple

from jose import jwt, JWTError
from pyotp import random_base32, TOTP

from src.utils.date_time import DateTime


def random_number_with_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


class Security:

    @staticmethod
    def hash_password(password: Union[bytes, str]) -> str:
        if isinstance(password, str):
            password = password.encode('utf-8')
        sha = sha256()
        sha.update(password)
        return sha.hexdigest()

    @staticmethod
    def encode_token(data: dict, hours: int = 1) -> str:
        data['exp'] = DateTime.expiration_date(hours=hours)
        return jwt.encode(
            data,
            environ.get('SECRET_KEY'),
            environ.get('ALGORITHM')
        )

    @staticmethod
    def decode_token(token: str) -> Tuple[Union[dict, None], bool]:
        """
        Decode Token and verify if email key exist in data, otherwise return a
        false if is valid

        :param token:
        :return:
        """
        try:
            data = jwt.decode(
                token,
                environ.get('SECRET_KEY'),
                environ.get('ALGORITHM')
            )
            if not data.get('email'):
                return None, False
            return data, True
        except JWTError:
            return None, False

    @staticmethod
    def create_otp_key():
        return random_base32()

    @staticmethod
    def create_otp_url(otp_code: str, email: str):
        return TOTP(otp_code).provisioning_uri(email)
