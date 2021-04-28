from unittest import TestCase
from unittest.mock import Mock, patch

from src.utils.security import Security


def solve_path(path: str):
    source = 'src.utils.security'
    return ".".join([source, path])


class SecurityHashTestCase(TestCase):

    def test_hash_password_string(self):
        text = 'Any String'

        result = Security.hash_password(text)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    def test_hash_password_bytes(self):
        text = 'Any String'.encode('utf-8')

        result = Security.hash_password(text)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)


class SecurityTokenTestCase(TestCase):

    def setUp(self):
        self.secret_key = 'Any Secret'
        self.secret_algorithm = 'HS512'
        self.token_test = (
            'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwib'
            'mFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJlbWFpbCI6InRlc3RAdGV'
            'zdC5jb20ifQ.YPnYQRBTtDJlCZVgPm5r2V6l0gvFqaf55RijifMkO4Hf3XMZM9qQ5w'
            'dhZzAwJQlCYI70pj038YXPqorEHQY6nQ'
        )

    @patch(solve_path('secrets'))
    def test_encode_token_successful(self, mock_secrets: Mock):
        mock_secrets.get.side_effect = [self.secret_key, self.secret_algorithm]

        result = Security.encode_token({}, 20)

        self.assertIsInstance(result, str)

    @patch(solve_path('secrets'))
    def test_decode_token_successful(self, mock_secrets: Mock):
        mock_secrets.get.side_effect = [self.secret_key, self.secret_algorithm]

        result = Security.decode_token(self.token_test)

        self.assertIsInstance(result, tuple)
        self.assertIsNotNone(result[0])
        self.assertTrue(result[1])

    @patch(solve_path('secrets'))
    def test_decode_token_invalid_key(self, mock_secrets: Mock):
        mock_secrets.get.side_effect = ['Invalid Key', self.secret_algorithm]

        result = Security.decode_token(self.token_test)

        self.assertIsInstance(result, tuple)
        self.assertIsNone(result[0])
        self.assertFalse(result[1])


class SecurityOtpTestCase(TestCase):

    def test_create_otp_key(self):
        result = Security.create_otp_key()

        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)

    def test_create_otp_url(self):
        result = Security.create_otp_url('123456', 'test@test.com')

        self.assertIsInstance(result, str)
