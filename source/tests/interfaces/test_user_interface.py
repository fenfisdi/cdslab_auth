from unittest import TestCase
from unittest.mock import patch, Mock

import pymongo
from mongomock import patch as db_path, ObjectId
from pymongo.results import InsertOneResult

from source.interfaces.user_interface import UserInterface


def solve_path(path: str):
    source = 'source.interfaces.user_interface'
    return ".".join([source, path])


class UserInterfaceTestCase(TestCase):

    @db_path(servers=(('mongodb.example.com', 27017),))
    def setUp(self):
        self.client = pymongo.MongoClient('mongodb.example.com')
        self.test_mock = self.client.get_database('test')
        self.test_client = self.test_mock.get_collection('user')

        self.example = self.test_client.insert_one({'email': 'test@test.com'})

    def tearDown(self):
        self.client.close()

    @patch(solve_path('get_db_connection'))
    def test_retrieve_user_ok(self, mock_db: Mock):
        mock_db.return_value = self.test_mock

        result = UserInterface.retrieve_user(email='test@test.com')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

    @patch(solve_path('get_db_connection'))
    def test_retrieve_user_not_found(self, mock_db: Mock):
        mock_db.return_value = self.test_mock

        result = UserInterface.retrieve_user(email='test1@test.com')

        self.assertIsNone(result)

    @patch(solve_path('get_db_connection'))
    def test_insert_user_ok(self, mock_db: Mock):
        mock_db.return_value = self.test_mock

        user = {
            'name': 'bot_test',
            'email': 'bot@test.com',
        }

        result = UserInterface.insert_user(user)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, InsertOneResult)
        self.assertIsInstance(result.inserted_id, ObjectId)

    @patch(solve_path('get_db_connection'))
    def test_update_user_state_ok(self, mock_db: Mock):
        mock_db.return_value = self.test_mock

        user_data = {
            'name': 'bot',
            'gender': 'M',
            'cc': 8372394723,
        }

        result = UserInterface.update_user_state(
            user_data,
            str(self.example.inserted_id)
        )

        self.assertTrue(result)

    @patch(solve_path('get_db_connection'))
    def test_update_user_state_empty(self, mock_db: Mock):
        mock_db.return_value = self.test_mock

        result = UserInterface.update_user_state({}, '12345')

        self.assertFalse(result)

    @patch(solve_path('get_db_connection'))
    def test_update_user_state_fail(self, mock_db: Mock):
        mock_db.return_value = self.test_mock

        user_data = {
            'name': 'bot',
            'gender': 'F',
            'cc': 27312937485,
        }

        result = UserInterface.update_user_state(
            user_data,
            str(ObjectId())
        )

        self.assertFalse(result)
