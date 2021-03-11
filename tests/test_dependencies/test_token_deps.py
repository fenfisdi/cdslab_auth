import pytest

from dependencies.token_deps import validate_access_token_email
from tests.utils.token import generate_random_token, generate_fake_token_with_other_secret_key
from tests.utils.utils import random_email, random_lower_string

def test_validate_token_type():
    assert validate_access_token_email(generate_random_token("email", random_email()))

@pytest.mark.xfail(reason = "Invalid token")
def test_invalid_secret_key_token():
    assert validate_access_token_email(generate_fake_token_with_other_secret_key("email", random_email()))

@pytest.mark.xfail(reason = "Invalid type")
def test_invalid_key_argument_token():
    assert validate_access_token_email(generate_random_token(random_lower_string(),random_email()))