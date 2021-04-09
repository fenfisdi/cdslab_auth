from hashlib import sha256
from random import randint
from typing import Union


def random_number_with_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


class Security:

    @staticmethod
    def hash_password(password: Union[bytes, str]) -> str:
        if isinstance(password, str):
            password = password.encode('utf-8')
        sha = sha256()
        sha.update(password)
        return sha.hexdigest()
