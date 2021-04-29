from unittest import TestCase
from unittest.mock import patch, Mock

from src.services import UserAPI


def solve_path(path: str):
    source = 'src.services.user_api'
    return ".".join([source, path])


class UserApiTestCase(TestCase):

    @patch.object(UserAPI, 'request')
    @patch.object(UserAPI, 'api_url')
    def test_create_user_successful(self, mock_settings: Mock, mock_api: Mock):
        mock_settings.return_value = {'USER_API': 'https://myapi'}
        mock_api = "asd"
        result = UserAPI.create_user({})