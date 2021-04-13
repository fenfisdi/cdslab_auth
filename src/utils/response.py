from typing import Optional

from fastapi.responses import UJSONResponse as FastAPIResponse
from requests.models import Response


class UJSONResponse(FastAPIResponse):
    def __init__(self, message: str, status_code: int,
                 data: Optional[dict] = None):
        response = dict(
            message=message,
            status_code=status_code,
            data=data,
        )
        super().__init__(response, status_code)


def to_response(response: Response) -> UJSONResponse:
    data = response.text
    message = 'API Error'
    if response.headers.get('content-type') == 'application/json':
        data = response.json()
        data = data.get('data', data)
        message = data.get('message', message)
    return UJSONResponse(message, response.status_code, data)
