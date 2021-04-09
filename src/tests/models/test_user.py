from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock

from pydantic.error_wrappers import ValidationError
from pydantic.main import BaseModel

from src.models.user import BaseUser, User


def solve_path(path: str):
    source = 'src.models.user'
    return ".".join([source, path])


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.settings = {
            'REGION_CODE': '57',
            'COUNTRY_CODE': '57',
        }
        self.user_data = {
            'email': 'test@test.com',
            'name': 'bot',
            'last_name': 'test',
            'institution': 'university',
            'institution_afiliation': 'student',
            'profession': 'engineer',
            'sex': 'F',
            'phone_number': '+573214849484',
            'date_of_birth': datetime(2021, 4, 5),
        }

    @patch(solve_path('settings'))
    def test_base_user_ok(self, mock_settings: Mock):
        mock_settings.return_value = self.settings

        user = BaseUser(**self.user_data)

        self.assertIsInstance(user, BaseModel)

    def test_base_user_empty(self):
        with self.assertRaises(ValidationError):
            BaseUser()

    @patch(solve_path('settings'))
    def test_base_user_fail_gender(self, mock_settings: Mock):
        mock_settings.return_value = self.settings
        fail_data = self.user_data.copy()
        fail_data['sex'] = 'T'

        with self.assertRaises(ValidationError):
            BaseUser(**fail_data)

    @patch(solve_path('settings'))
    def test_base_user_fail_phone_null(self, mock_settings: Mock):
        mock_settings.return_value = self.settings
        fail_data = self.user_data.copy()
        fail_data['phone_number'] = None

        with self.assertRaises(ValidationError):
            BaseUser(**fail_data)

    @patch(solve_path('settings'))
    def test_base_user_fail_phone_1(self, mock_settings: Mock):
        mock_settings.return_value = self.settings
        fail_data = self.user_data.copy()
        fail_data['phone_number'] = '3215234231'

        with self.assertRaises(ValidationError):
            BaseUser(**fail_data)

    @patch(solve_path('settings'))
    def test_base_user_fail_phone_2(self, mock_settings: Mock):
        mock_settings.return_value = self.settings
        fail_data = self.user_data.copy()
        fail_data['phone_number'] = '+3214'

        with self.assertRaises(ValidationError):
            BaseUser(**fail_data)

    @patch(solve_path('settings'))
    def test_base_user_fail_phone_3(self, mock_settings: Mock):
        mock_settings.return_value = self.settings
        fail_data = self.user_data.copy()
        fail_data['phone_number'] = '+3212412341'

        with self.assertRaises(ValidationError):
            BaseUser(**fail_data)


class UserTestCase(TestCase):

    def setUp(self):
        self.settings = {
            'REGION_CODE': '57',
            'COUNTRY_CODE': '57',
        }
        self.user_data = {
            'email': 'test@test.com',
            'name': 'bot',
            'last_name': 'test',
            'institution': 'university',
            'institution_afiliation': 'student',
            'profession': 'engineer',
            'sex': 'F',
            'phone_number': '+573214849484',
            'date_of_birth': datetime(2021, 4, 5),
            'password': 'string',
            'verify_password': 'string',
        }

    @patch(solve_path('settings'))
    def test_user_ok(self, mock_settings: Mock):
        mock_settings.return_value = self.settings

        user = User(**self.user_data)

        self.assertIsInstance(user, User)

    @patch(solve_path('settings'))
    def test_user_invalid_pass(self, mock_settings: Mock):
        mock_settings.return_value = self.settings
        fail_data = self.user_data.copy()
        fail_data['password'] = 'gnirts'

        with self.assertRaises(ValidationError):
            User(**fail_data)
