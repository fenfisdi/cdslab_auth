from os import environ

from src.utils.date_time import DateTime
from .service import API, APIService


class ErrorAPI:
    api_url = environ.get('ERROR_API')
    request = APIService(API(api_url))

    @classmethod
    def report_error(cls, message: str, code: int) -> None:
        body = {
            'application': 'configuration app',
            'date': DateTime.current_datetime().isoformat(),
            'message': message,
            'code': code,
        }
        cls.request.post(
            '/error',
            data=body
        )
