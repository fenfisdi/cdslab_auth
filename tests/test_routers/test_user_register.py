from fastapi.testclient import TestClient
from dotenv import dotenv_values

from db_connection import users
from main import app
from dependencies import qr_deps, token_deps
from tests.utils.utils import random_email, random_lower_string
from tests.utils.token import generate_random_token, generate_fake_token_with_other_secret_key
from tests.utils.user import *


settings = dotenv_values(".env")

client = TestClient(app)

# Test POST save_user path

def test_created_correct_user():
    random_user = created_random_user("", "")
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=random_user)
    if users.find_one():
        users.delete_one({"email": random_user["email"]})
    assert response.status_code == 200

def test_register_user_invalid_email():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('email', random_lower_string()))
    assert response.status_code >= 400

def test_register_user_invalid_name():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('name', random_email()))
    assert response.status_code >= 400

def test_register_user_invalid_last_name():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('last_name', random_email()))
    assert response.status_code >= 400

def test_register_user_invalid_sex():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('sex', random_lower_string()))
    assert response.status_code >= 400

def test_register_user_invalid_phone_number():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('phone_number', random_lower_string()))
    assert response.status_code >= 400

def test_register_user_invalid_birth_date():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('date_of_birth', random_lower_string()))
    assert response.status_code >= 400

def test_register_user_password_not_match():
    response = client.post(f"{settings['REGISTER_PATH']}/save_user", json=created_random_user('verify_password', random_lower_string()))
    assert response.status_code >= 400

# Test POST qr_validation path

def test_valid_user_qr():
    response = client.post(f"{settings['REGISTER_PATH']}/qr_validation", json={"email":"pipin@gmail.com", "qr_value": qr_deps.get_value_key_qr("JL4BEB76RXBFLPRUUWMPO5BUSC7OHTEL")})
    assert response.status_code == 200

def test_invalid_user_qr():
    response = client.post(f"{settings['REGISTER_PATH']}/qr_validation", json={"email":"pipin@gmail.com", "qr_value": random_lower_string()})
    assert response.status_code >= 400

# Test GET token_email

def test_activate_valid_account():
    user_in_db = users.find_one({},{'email': 1})
    user_in_db = user_in_db['email']
    token = token_deps.generate_token_jwt({'email': user_in_db})
    response = client.get(f"{settings['REGISTER_PATH']}/{token['access_token']}")
    assert response.status_code == 200

def test_activate_invalid_account():
    response = client.get(f"{settings['REGISTER_PATH']}/{token_deps.generate_token_jwt({'email': random_email()})['access_token']}")
    assert response.status_code >= 400

