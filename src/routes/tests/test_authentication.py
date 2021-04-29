from unittest.mock import patch, Mock

from fastapi.testclient import TestClient

from src.routes.tests.base import RoutesTestCase
from src.utils.response import UJSONResponse


def solve_path(path: str):
    source = 'src.routes.authentication'
    return ".".join([source, path])


class LoginAuthTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='login@test.com',
            password='any_password'
        )
        self.route = '/login'

    @patch(solve_path('UserAPI'))
    def test_login_auth_successful(self, mock_api: Mock):
        valid_data = dict(data=dict())
        mock_api.validate_credentials.return_value = valid_data, False

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('UserAPI'))
    def test_login_auth_invalid(self, mock_api: Mock):
        response = UJSONResponse('message', 400)
        mock_api.validate_credentials.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)


class LoginOTPAuthTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='login@test.com',
            otp_code='192837'
        )
        self.route = '/login/otp'

    @patch(solve_path('Security'))
    @patch(solve_path('ValidateOTPUseCase'))
    def test_login_otp_auth_successful(
        self,
        mock_use_case: Mock,
        mock_security: Mock
    ):
        mock_use_case.handle.return_value = None, False
        mock_security.encode_token.return_value = 'myToken'

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('Security'))
    @patch(solve_path('ValidateOTPUseCase'))
    def test_login_otp_auth_successful(
            self,
            mock_use_case: Mock,
            mock_security: Mock
    ):
        mock_use_case.handle.return_value = None, False
        mock_security.encode_token.return_value = 'myToken'

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('ValidateOTPUseCase'))
    def test_login_otp_auth_invalid(self, mock_use_case: Mock):
        response = UJSONResponse('message', 400)
        mock_use_case.handle.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)


class CreateSecurityCodeTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='login@test.com'
        )
        self.route = '/login/recovery_code'

    @patch(solve_path('UserAPI'))
    def test_create_security_code_successful(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        mock_api.save_security_code.return_value = None, False

        result = self.client.post(self.route, params=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('UserAPI'))
    def test_create_security_code_not_found(self, mock_api: Mock):
        response = UJSONResponse('message', 404)
        mock_api.find_user.return_value = response, True

        result = self.client.post(self.route, params=self.valid_data)

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    def test_create_security_code_invalid_code(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = UJSONResponse('message', 400)
        mock_api.save_security_code.return_value = response, True

        result = self.client.post(self.route, params=self.valid_data)

        self.verify_response(result, 400)


class ValidateSecurityCodeTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='login@test.com',
            security_code='192734'
        )
        self.route = '/login/validate_code'

    @patch(solve_path('UserAPI'))
    def test_validate_security_code_successful(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        user_data = {'data': {'security_code': '192734'}}
        mock_api.find_security_code.return_value = user_data, False

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('UserAPI'))
    def test_validate_security_code_not_found(self, mock_api: Mock):
        response = UJSONResponse('message', 404)
        mock_api.find_user.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    def test_validate_security_code_invalid_api(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = UJSONResponse('message', 400)
        mock_api.find_security_code.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)

    @patch(solve_path('UserAPI'))
    def test_validate_security_code_invalid(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        user_data = {'data': {'security_code': '456928'}}
        mock_api.find_security_code.return_value = user_data, False

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)


class RecoverPasswordTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='login@test.com',
            password='192734',
            verify_password='192734'
        )
        self.route = '/login/recover_password'

    @patch(solve_path('UserAPI'))
    def test_recover_password_successful(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        mock_api.update_password.return_value = None, False

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('UserAPI'))
    def test_recover_password_not_found(self, mock_api: Mock):
        response = UJSONResponse('message', 404)
        mock_api.find_user.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    def test_recover_password_cant_update(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = UJSONResponse('message', 400)
        mock_api.update_password.return_value = response, True

        result = self.client.post(self.route, json=self.valid_data)

        self.verify_response(result, 400)


class FindSecurityQuestionTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='login@test.com'
        )
        self.route = '/login/security_question'

    @patch(solve_path('UserAPI'))
    def test_find_security_question_successful(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        data = {'data': [{'question': '1'}, {'question': '2'}]}
        mock_api.find_security_questions.return_value = data, False

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 200)

    @patch(solve_path('UserAPI'))
    def test_find_security_question_user_not_found(self, mock_api: Mock):
        response = UJSONResponse('message', 404)
        mock_api.find_user.return_value = response, True

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    def test_find_security_question_not_found(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = UJSONResponse('message', 400)
        mock_api.find_security_questions.return_value = response, True

        result = self.client.get(self.route, params=self.valid_data)

        self.verify_response(result, 400)


class ValidateSecurityQuestionTestCase(RoutesTestCase):

    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = [
            {
                'question': 'q1',
                'answer': 'a1',
            },
            {
                'question': 'q2',
                'answer': 'a2',
            },
        ]
        self.valid_params = {
            'email': 'test@test.com',
        }
        self.route = '/login/security_questions'

    @patch(solve_path('UserAPI'))
    def test_validate_security_questions_successful(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = {'data': self.valid_data}
        mock_api.find_security_questions.return_value = response, False
        response = {'data': {'otp_code': '172394'}}
        mock_api.find_otp_key.return_value = response, False

        result = self.client.post(
            self.route,
            json=self.valid_data,
            params=self.valid_params
        )

        self.verify_response(result, 200)

    @patch(solve_path('UserAPI'))
    def test_validate_security_questions_user_not_found(self, mock_api: Mock):
        response = UJSONResponse('not_found', 404)
        mock_api.find_user.return_value = response, True

        result = self.client.post(
            self.route,
            json=self.valid_data,
            params=self.valid_params
        )

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    def test_validate_security_questions_not_found(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = UJSONResponse('not_found', 404)
        mock_api.find_security_questions.return_value = response, True

        result = self.client.post(
            self.route,
            json=self.valid_data,
            params=self.valid_params
        )

        self.verify_response(result, 404)

    @patch(solve_path('UserAPI'))
    def test_validate_security_questions_invalid(self, mock_api: Mock):
        mock_api.find_user.return_value = None, False
        response = {'data': []}
        mock_api.find_security_questions.return_value = response, False

        result = self.client.post(
            self.route,
            json=self.valid_data,
            params=self.valid_params
        )

        self.verify_response(result, 400)





