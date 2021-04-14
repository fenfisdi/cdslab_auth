from src.config import settings
from src.utils.response import to_response
from src.utils.serializer import encode_request
from .service import API, APIService


class UserAPI:
    api_url = settings.get('USER_API')
    request = APIService(API(api_url))

    @classmethod
    def create_user(cls, user_data: dict):
        user_data = encode_request(user_data)
        response = cls.request.post('/user', user_data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def validate_user(cls, email: str):
        response = cls.request.get(f'/user/{email}/validate')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_otp_code(cls, email: str):
        response = cls.request.get(f'/user/{email}/otp')
        if not response.ok:
            return to_response(response), True
        return response.json(), False

    @classmethod
    def find_user(cls, email: str, invalid: bool = False):
        parameters = {
            'invalid': invalid,
        }
        response = cls.request.get(f'/user/{email}', parameters=parameters)
        if not response.ok:
            return to_response(response), True
        return response.json(), False
