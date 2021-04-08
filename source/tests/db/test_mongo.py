from unittest import TestCase
from unittest.mock import patch, Mock

from mongomock import patch as db_patch
from pymongo.database import Database

from source.db.mongo import get_db_connection


def solve_path(path: str):
    source = 'source.db.mongo'
    return ".".join([source, path])


class MongoTestCase(TestCase):

    @db_patch(servers=(('mongodb://mongodb.example.com', 27017),))
    @patch(solve_path('db_config'))
    def test_get_db_connection(self, mock_config: Mock):
        server = "mongodb://mongodb0.example.com:27017"
        mock_config.get.side_effect = [server, "test_db"]

        db = get_db_connection()

        self.assertIsInstance(db, Database)
