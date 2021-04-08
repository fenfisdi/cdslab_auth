from unittest import TestCase
from unittest.mock import patch, Mock

from source.dependencies.token_deps import (
    generate_token_jwt,
    validate_email_access_token
)


def solve_path(path: str):
    source = 'source.dependencies.token_deps'
    return ".".join([source, path])


class GenerateTokenTestCase(TestCase):

    @patch(solve_path('secrets'))
    def test_generate_token_ok(self, mock_setting: Mock):
        mock_setting.get.side_effect = ['secret', 'HS256']

        payload = {'email': 'test@test.com'}
        result = generate_token_jwt(payload)

        self.assertIsInstance(result, dict)
        self.assertIn('access_token', result)

    @patch(solve_path('secrets'))
    def test_generate_token_empty(self, mock_setting: Mock):
        mock_setting.get.side_effect = ['secret', 'HS256']

        result = generate_token_jwt({})

        self.assertIsInstance(result, dict)
        self.assertIn('access_token', result)


class ValidateTokenTestCase(TestCase):

    @patch(solve_path('secrets'))
    def test_validate_token_ok(self, mock_setting: Mock):
        side_effect = ['secret', 'HS256']
        mock_setting.get.side_effect = side_effect
        payload = {'email': 'test@test.com'}
        result = generate_token_jwt(payload)
        mock_setting.get.side_effect = side_effect
        test_token = result.get('access_token')

        result = validate_email_access_token(test_token)

        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], dict)
        self.assertIn('email', result[1])

    @patch(solve_path('secrets'))
    def test_validate_token_fail(self, mock_setting: Mock):
        side_effect = ['secret', 'HS256']
        mock_setting.get.side_effect = side_effect

        result = validate_email_access_token('abc1234')

        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], bool)
        self.assertIsNone(result[1])
