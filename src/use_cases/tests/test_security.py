from unittest import TestCase
from unittest.mock import patch, Mock

from pyotp import TOTP

from src.use_cases.security import ValidateOTPUseCase


def solve_path(path: str):
    source = 'src.use_cases.security'
    return ".".join([source, path])


class ValidateOTPUseCaseTestCase(TestCase):

    def setUp(self):
        self.email = 'test1@test.com'
        self.otp_key = '23SPBFVNX3ZLLDGZF5LZ5XKVWDNT2F7C'
        self.otp_code = TOTP(self.otp_key).now()

    @patch(solve_path('UserAPI'))
    def test_validate_otp_use_case_successful(self, user_api: Mock):

        user_api.find_user.return_value = Mock(), False
        mock_otp = dict(data=dict(otp_code=self.otp_key))
        user_api.find_otp_key.return_value = mock_otp, False

        result = ValidateOTPUseCase.handle(self.email, self.otp_code)

        self.assertIsInstance(result, tuple)
        self.assertIsNone(result[0])
        self.assertFalse(result[1])

    @patch(solve_path('UserAPI'))
    def test_validate_otp_use_case_user_not_found(self, user_api: Mock):
        user_api.find_user.return_value = Mock(), True

        result = ValidateOTPUseCase.handle(self.email, self.otp_code)

        self.assertIsInstance(result, tuple)
        self.assertIsNotNone(result[0])
        self.assertTrue(result[1])

    @patch(solve_path('UserAPI'))
    def test_validate_otp_use_case_otp_not_found(self, user_api: Mock):
        user_api.find_user.return_value = Mock(), False
        user_api.find_otp_key.return_value = Mock(), True

        result = ValidateOTPUseCase.handle(self.email, self.otp_code)

        self.assertIsInstance(result, tuple)
        self.assertIsNotNone(result[0])
        self.assertTrue(result[1])

    @patch(solve_path('UserAPI'))
    def test_validate_otp_use_case_otp_invalid(self, user_api: Mock):
        user_api.find_user.return_value = Mock(), False
        mock_otp = dict(data=dict(otp_code=self.otp_key))
        user_api.find_otp_key.return_value = mock_otp, False

        result = ValidateOTPUseCase.handle(self.email, '122345')

        self.assertIsInstance(result, tuple)
        self.assertIsNotNone(result[0])
        self.assertTrue(result[1])
