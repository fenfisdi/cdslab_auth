from fastapi.testclient import TestClient
from dotenv import dotenv_values

from main import app
from db_connection import users
from dependencies import user_deps, qr_deps
from models import user
from tests.utils.utils import random_email, random_lower_string
from tests.utils.token import generate_random_token, generate_fake_token_with_other_secret_key


settings = dotenv_values(".env")

client = TestClient(app)

# Test POST LoginAuthentication

def test_valid_password():
    response = client.post(f"/auth/loginAuthentication", json={"email": users.find_one({},{'email': 1})['email'], "password": "12345"})
    assert response.status_code == 200

def test_incorrect_password():
    response = client.post(f"/auth/loginAuthentication", json={"email": users.find_one({},{'email': 1})['email'], "password": "1234567"})
    assert response.status_code >= 400

def test_incorrect_email():
    response = client.post(f"/auth/loginAuthentication", json={"email": random_email(), "password": "123456"})
    #print(response.json())
    assert response.status_code >= 400

def test_incorrect_type_password():
    response = client.post(f"/auth/loginAuthentication", json={"email": users.find_one({},{'email': 1})['email'], "password": 123544})
    #print(response.json())
    assert response.status_code == 404

def test_invalid_email():
    response = client.post(f"/auth/loginAuthentication", json={"email": random_lower_string(), "password": 123544})
    assert response.status_code >= 400

# Test POST qrAuthentication

def test_incorrect_qr_value_in_qr_auth():

    response = client.post(f"/auth/qrAuthentication",
                           json={"email": users.find_one({},{'email': 1})['email'], 
                                "qr_value": random_lower_string()})

    assert response.status_code >= 400


def test_correct_qr_value_in_qr_auth():
    email = users.find_one({},{'email': 1})['email']
    qr_value = users.find_one({},{'key_qr': 1})['key_qr']
    print(qr_deps.get_value_key_qr(qr_value))
    response = client.post(f"/auth/qrAuthentication",
                           json={"email": email, 
                                "qr_value": str(qr_deps.get_value_key_qr(qr_value))})

    assert response.status_code == 200