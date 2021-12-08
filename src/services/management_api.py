from os import environ
from typing import Tuple, Union

from src.utils.response import UJSONResponse, to_response
from src.utils.serializer import encode_request
from .service import APIService, API


class ManagementAPI:
    api_url = environ.get('MANAGEMENT_API')
    request = APIService(API(api_url))

    @classmethod
    def send_email(
        cls,
        email_data: dict
    ) -> Tuple[Union[dict, UJSONResponse], bool]:
        """
        Send information to the user email

        :param email_data: email information to send to the user, this dict
        should content fields as (email, receiver, subject, message), this
        fields are mandatory.

        """
        data = encode_request(email_data)
        response = cls.request.post('/email/notification', data)
        if not response.ok:
            return to_response(response), True
        return response.json(), False
