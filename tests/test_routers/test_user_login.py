from fastapi.testclient import TestClient
from dotenv import dotenv_values

from main import app
from db_connection import users
from dependencies import user_deps
from models import user
from tests.utils.utils import random_email, random_lower_string
from tests.utils.token import generate_random_token, generate_fake_token_with_other_secret_key


settings = dotenv_values(".env")

client = TestClient(app)

# Test POST LoginAuthentication

def test_incorrect_password():
    response = client.post(f"/auth/loginAuthentication", json={"email": "pinpinela@example.com", "password": "123456"})
    #print(response.json())
    assert response.status_code == 404

def test_incorrect_email():
    response = client.post(f"/auth/loginAuthentication", json={"email": "andresig@example.com", "password": "123456"})
    #print(response.json())
    assert response.status_code == 404

def test_incorrect_type_password():
    response = client.post(f"/auth/loginAuthentication", json={"email": "andresig@example.com", "password": 123544})
    #print(response.json())
    assert response.status_code == 404

def test_invalid_email():
    response = client.post(f"/auth/loginAuthentication", json={"email": "andresigexample.com", "password": 123544})
    assert response.status_code >= 400

# Test POST LoginAuthentication

"""
def test_request_registration_invalid_email():
    response = client.post(f"{settings['REGISTER_PATH']}/", json={"email": random_lower_string()})
    assert response.status_code == 422

def test_request_registration_registered_user():
    response = client.post(f"{settings['REGISTER_PATH']}/", json={"email": users.find_one()["email"]})
    assert response.status_code == 404
    assert response.json() == {"detail": "User already exists"}

# Test GET method

def test_read_email_valid_token():
   response = client.get(f"{settings['REGISTER_PATH']}/{generate_random_token('email', random_email())}")
   assert response.status_code == 200

def test_read_email_invalid_token():
   response = client.get(f"{settings['REGISTER_PATH']}/{generate_fake_token_with_other_secret_key('email', random_email())}")
   assert response.status_code == 401
"""