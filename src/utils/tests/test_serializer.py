from datetime import datetime
from unittest import TestCase

from ujson import loads

from src.utils.serializer import JSONEncoder, encode_request


class JsonEncoderTestCase(TestCase):

    def test_bson_encoder_ok(self):
        data = {
            'int': 1,
            'str': 'any_word',
            'datetime': datetime(2021, 2, 3)
        }
        result = JSONEncoder().encode(data)

        self.assertIsInstance(result, str)
        dict_result = loads(result)
        self.assertIsInstance(dict_result.get('datetime'), str)


class EncodeRequestTestCase(TestCase):

    def test_encode_request(self):
        data = {
            'str': 'Any String',
            'datetime': datetime.now(),
        }

        result = encode_request(data)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result.get('datetime'), str)
