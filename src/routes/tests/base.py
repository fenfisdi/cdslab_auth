from unittest import TestCase

from requests import Response


class RoutesTestCase(TestCase):

    def verify_response(
        self,
        result: Response,
        status_code: int,
        has_data: bool = False
    ):
        self.assertEqual(status_code, result.status_code)
        self.assertEqual(result.headers.get('content-type'), 'application/json')
        data_json: dict = result.json()
        print(data_json)
