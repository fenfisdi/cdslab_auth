import pytest

from models import user
from dependencies import user_deps
from tests.utils import utils

# Test tokenize_email function

def test_tokenize_email():
    assert user_deps.tokenize_email(user.applicant_user(email = utils.random_email()))

@pytest.mark.xfail(reason = "Invalid type mail")
def test_tokenize_email_Invalid_type():
    assert user_deps.tokenize_email({"email": 14156})

@pytest.mark.xfail(reason = "Invalid type email")
def test_tokenize_email_Invalid_type2():
    assert user_deps.tokenize_email({"email": [utils.random_email()]})

@pytest.mark.xfail(reason = "Invalid type email")
def test_tokenize_email_Invalid_type3():
    assert user_deps.tokenize_email({"email" : {"email": utils.random_email()}})