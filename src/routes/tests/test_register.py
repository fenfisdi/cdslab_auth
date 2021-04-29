from unittest.mock import patch, Mock

from fastapi.testclient import TestClient

from src.routes.tests.base import RoutesTestCase
from src.utils.response import UJSONResponse


def solve_path(path: str):
    source = 'src.routes.register'
    return ".".join([source, path])


class CreateUserTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            name="test name",
            last_name="test last name",
            phone=1829382738,
            phone_prefix="+1",
            institution="string",
            institution_role="string",
            profession="string",
            gender="M",
            birthday="2019-08-24T14:15:22Z",
            email="user@example.com",
            password="string",
            security_questions=[]
        )
        self.route = '/register/user'

    @patch(solve_path('UserAPI'))
    @patch(solve_path('Security'))
    def test_create_user_successful(self, mock_security: Mock, mock_api: Mock):
        mock_security.create_otp_key.return_value = '123456'
        mock_security.create_otp_url.return_value = 'url'
        mock_api.create_user.return_value = {
            'data': {'otp_code': '12345'}
        }, False

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 201)

    @patch(solve_path('UserAPI'))
    @patch(solve_path('Security'))
    def test_create_user_exist(self, mock_security: Mock, mock_api: Mock):
        mock_security.create_otp_key.return_value = '123456'
        response = UJSONResponse('Message', 400)
        mock_api.create_user.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)


class ValidateUserOTPTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(email='test2@test.com', otp_code='123456')

        self.route = '/register/user/otp'

    @patch(solve_path('Security'))
    @patch(solve_path('ValidateOTPUseCase'))
    def test_validate_user_otp_successful(
        self,
        mock_use_case: Mock,
        mock_security: Mock
    ):
        mock_use_case.handle.return_value = Mock(), False
        mock_security.encode_token.return_value = 'myToken'

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('ValidateOTPUseCase'))
    def test_validate_user_otp_invalid(self, mock_use_case: Mock):
        response = UJSONResponse('message', 400)
        mock_use_case.handle.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)


class ValidateUserEmailTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(token='myToken')
        self.token_data = dict(email='test@test.co')

        self.route = '/register/user/email'

    @patch(solve_path('UserAPI'))
    @patch(solve_path('Security'))
    def test_validate_user_email_successful(
        self,
        mock_security: Mock,
        mock_api: Mock
    ):
        api_data = dict(data=self.token_data)
        mock_security.decode_token.return_value = self.token_data, True
        mock_api.find_user.return_value = api_data, False
        mock_api.validate_user.return_value = None, True

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('Security'))
    def test_validate_user_email_invalid_token(self, mock_security: Mock):
        mock_security.decode_token.return_value = None, False

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 422)

    @patch(solve_path('UserAPI'))
    @patch(solve_path('Security'))
    def test_validate_user_found(
            self,
            mock_security: Mock,
            mock_api: Mock
    ):
        mock_security.decode_token.return_value = self.token_data, True
        response = UJSONResponse('message', 400)
        mock_api.find_user.return_value = response, True

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 400)

    @patch(solve_path('UserAPI'))
    @patch(solve_path('Security'))
    def test_validate_user_email_invalid(
            self,
            mock_security: Mock,
            mock_api: Mock
    ):
        api_data = dict(data=dict(email='test2@test.co'))
        mock_security.decode_token.return_value = self.token_data, True
        mock_api.find_user.return_value = api_data, False

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    @patch(solve_path('Security'))
    def test_validate_user_email_not_valid(
            self,
            mock_security: Mock,
            mock_api: Mock
    ):
        api_data = dict(data=self.token_data)
        mock_security.decode_token.return_value = self.token_data, True
        mock_api.find_user.return_value = api_data, False
        response = UJSONResponse('message', 400)
        mock_api.validate_user.return_value = response, False

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 400)









