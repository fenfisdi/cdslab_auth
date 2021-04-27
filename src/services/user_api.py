from typing import Union, Tuple

from src.config import settings
from src.utils.response import UJSONResponse
from src.utils.response import to_response
from src.utils.serializer import encode_request
from .service import API, APIService


class UserAPI:
    api_url = settings.get('USER_API')
    request = APIService(API(api_url))

    @classmethod
    def create_user(
            cls,
            user_data: dict
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Create and save user data to storage in User API, could return 400 if
        user exist

        :param user_data: user information to save
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
        Validate user state to valid user

        :param email:
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


        :param email: user email to find otp key
        :return:
        """
        response = cls.request.get(f'/user/{email}/otp')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_user(
            cls,
            email: str,
            invalid: bool = False
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        parameters = {
            'invalid': invalid,
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
        response = cls.request.get(f'/user/{email}/security_code')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_security_questions(
            cls,
            email: str
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
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

        :param data:
        :return:
        """
        response = cls.request.post(f'/user/password', data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False
