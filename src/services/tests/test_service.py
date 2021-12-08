from unittest import TestCase
from unittest.mock import patch, Mock

from src.services.service import API, APIService


def solve_path(path: str):
    source = 'src.services.service'
    return ".".join([source, path])


class ApiServiceTestCase(TestCase):

    def setUp(self):
        api = API('https://test.net')
        self.api_service = APIService(api=api)

    @patch(solve_path('Session.send'))
    def test_post_successful(self, mock_session: Mock):
        mock_session.send.return_value = Mock()
        self.api_service.post('/any/endpoint', {})

        mock_session.assert_called()

    @patch(solve_path('Session.send'))
    def test_get_successful(self, mock_session: Mock):
        mock_session.send.return_value = Mock()

        self.api_service.get('/any/endpoint', {})

        mock_session.assert_called()
