import pytest

from models import user
from dependencies import user_deps
from tests.utils import utils
# Test application_user class

# Testing Emailstr field

def test_valid_email_user():
    assert user.applicant_user(email = utils.random_email())

# These tests for email should be fail always

@pytest.mark.xfail(reason = "Invalid email")
def test_invalid_email_without_dot():
    assert user.applicant_user(email = "user@examplecom")

@pytest.mark.xfail(reason = "Invalid email")
def test_invalid_email_without_at_sign():
    assert user.applicant_user(email = "userexample.com")

@pytest.mark.xfail(reason = "Invalid email")
def test_invalid_email_without_structure():
    assert user.applicant_user(email = "user@.com")

@pytest.mark.xfail(reason = "Invalid email")
def test_invalid_email_invalid_type():
    assert user.applicant_user(email = 121313254)

@pytest.mark.xfail(reason = "Invalid email")
def test_invalid_email_empty_field():
    assert user.applicant_user(email = "")

