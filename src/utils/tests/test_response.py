from unittest import TestCase
from unittest.mock import Mock

from src.utils.response import UJSONResponse, to_response


class UJSONResponseTestCase(TestCase):

    def test_response_sucessfull(self):
        message = 'Any Message'
        status = 200

        result = UJSONResponse(message, status)

        self.assertIsInstance(result, UJSONResponse)
        self.assertIsNotNone(result.body)


class ToResponseTestCase(TestCase):

    def test_to_response_sucessfull(self):
        response = Mock(
            text='{"hi": "everyone"}',
            headers={
                'content-type': 'application/json',
            }
        )
        response.json.return_value = {"hi": "everyone"}

        result = to_response(response)

        self.assertIsInstance(result, UJSONResponse)
