from os import environ
from typing import Union, Tuple

from src.utils.response import UJSONResponse
from src.utils.response import to_response
from src.utils.serializer import encode_request
from .service import API, APIService


class UserAPI:
    api_url = environ.get('USER_API')
    request = APIService(API(api_url))

    @classmethod
    def create_user(
            cls,
            user_data: dict
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Create and save user data to storage in User API, could return 400 if
        user exist.

        :param user_data: user information to save account
        """
        user_data = encode_request(user_data)
        response = cls.request.post('/user', user_data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def validate_user(
            cls,
            email: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Validate user, if is valid, user could be execute 3 party applications.

        :param email: user email to validate account.
        """
        response = cls.request.get(f'/user/{email}/validate')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_otp_key(
            cls,
            email: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        find account and otp key according with user email.

        :param email: user email to find otp key.
        """
        response = cls.request.get(f'/user/{email}/otp')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_user(
            cls,
            email: str,
            is_valid: bool = True
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Find all relevant information about user, according with the user email.

        :param email: user email to find in application.
        :param is_valid: if user had valid or invalid status.
        """
        parameters = {
            'is_valid': is_valid,
        }
        response = cls.request.get(f'/user/{email}', parameters=parameters)
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def validate_credentials(
            cls,
            data: dict
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Validate user credentials as email and password, according with user
        account.

        :param data: user data credentials as password and email.
        """
        response = cls.request.post(f'/user/credentials', data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def save_security_code(
            cls,
            email: str,
            code: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Update security code to recover account link with otp service.

        :param email: user email to update security code.
        :param code: security code to storage.
        """
        params = {
            'code': code,
        }
        response = cls.request.post(
            f'/user/{email}/security_code',
            parameters=params
        )
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_security_code(
            cls,
            email: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Recover account security code to recover account password.

        :param email: user email to recover account.
        """
        response = cls.request.get(f'/user/{email}/security_code')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_security_questions(
            cls,
            email: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Find security questions from user to recover account.

        :param email: user email to find security questions.
        """
        response = cls.request.get(f'/user/{email}/questions')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def update_password(
            cls,
            data: dict
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Update user account password.

        :param data: User information to update passwords as email.
        """
        response = cls.request.post(f'/user/password', data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False
