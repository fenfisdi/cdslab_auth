from fastapi.testclient import TestClient
from dotenv import dotenv_values
from operations.user_operations import *
from dependencies.qr_deps import *
from main import app
from db_connection import users
from dependencies import user_deps
from models import user
from tests.utils.utils import random_email, random_lower_string
from tests.utils.token import generate_random_token, generate_fake_token_with_other_secret_key

settings = dotenv_values(".env")


client = TestClient(app)

# Test POST route loginAuthentication


def test_incorrect_password():
    response = client.post(f"/auth/loginAuthentication",
                           json={"email": "pinpinela@example.com", "password": "123456"})
    # print(response.json())
    assert response.status_code == 404


def test_incorrect_email():
    response = client.post(f"/auth/loginAuthentication",
                           json={"email": "andresig@example.com", "password": "123456"})
    # print(response.json())
    assert response.status_code == 404


def test_incorrect_type_password():
    response = client.post(f"/auth/loginAuthentication",
                           json={"email": "andresig@example.com", "password": 123544})
    # print(response.json())
    assert response.status_code == 404


def test_invalid_email():
    response = client.post(f"/auth/loginAuthentication",
                           json={"email": "andresigexample.com", "password": 123544})
    assert response.status_code >= 400

# Test POST route qrAuthentication


def test_invalid_email():
    response = client.post(f"/auth/loginAuthentication",
                           json={"email": "andresigexample.com", "password": 123544})
    assert response.status_code >= 400


def test_incorrect_qr_value_in_qr_auth():

    response = client.post(f"/auth/qrAuthentication",
                           json={"email": "user@example.com", "qr_value": "123456"})

    assert response.status_code >= 400
