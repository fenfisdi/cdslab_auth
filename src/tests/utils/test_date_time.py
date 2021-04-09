from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock

from src.utils.date_time import DateTime


def solve_path(path: str):
    source = 'src.utils.date_time'
    return ".".join([source, path])


class DateTimeTestCase(TestCase):

    def setUp(self):
        self.current_date = datetime(2021, 2, 4, 19, 30)

    @patch(solve_path('datetime'))
    def test_current_date(self, mock_date: Mock):
        mock_date.utcnow.return_value = self.current_date

        current_datetime = DateTime.current_datetime()

        self.assertIsInstance(current_datetime, datetime)
        self.assertIsNotNone(current_datetime)
        self.assertEqual(current_datetime.year, 2021)
        self.assertEqual(current_datetime.month, 2)
        self.assertEqual(current_datetime.day, 4)

    @patch(solve_path('datetime'))
    def test_expiration_date_hour(self, mock_date: Mock):
        mock_date.utcnow.return_value = self.current_date

        expiration_datetime = DateTime.expiration_date(hours=24)

        self.assertIsInstance(expiration_datetime, datetime)
        self.assertIsNotNone(expiration_datetime)
        self.assertEqual(expiration_datetime.day, 5)

    @patch(solve_path('datetime'))
    def test_expiration_date_minute(self, mock_date: Mock):
        date = datetime(2021, 2, 4, 19, 30)
        mock_date.utcnow.return_value = date

        expiration_datetime = DateTime.expiration_date(minutes=60)

        self.assertIsInstance(expiration_datetime, datetime)
        self.assertIsNotNone(expiration_datetime)
        self.assertEqual(expiration_datetime.hour, 20)

