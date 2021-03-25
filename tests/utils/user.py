import datetime
import json

from models import user 
from tests.utils.utils import *


def created_random_user(key, value) -> dict:
    
    random_user =  {'email': random_email(),
                    'name': random_lower_string(),
                    'last_name': random_lower_string(),
                    'sex': 'M',
                    'phone_number': '+573001234567',
                    'institution': random_lower_string(),
                    'institution_afiliation': random_lower_string(),
                    'profession': random_lower_string(),
                    'date_of_birth': "2021-03-14T16:48:35.856Z",
                    'password': '12345',
                    'verify_password': '12345'
                    }
    random_user[key] = value
    return random_user