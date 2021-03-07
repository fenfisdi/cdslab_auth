from jose import jwt, JWTError
from dotenv import dotenv_values

secrets = dotenv_values(".secrets")

def generate_random_token(key, email):

    to_encode = {key: email}
    return jwt.encode(to_encode, secrets["SECRET_KEY"], algorithm=secrets["ALGORITHM"])

def generate_fake_token_with_other_secret_key(key, email):

    to_encode = {key: email}
    return jwt.encode(to_encode, secrets["f2fb66429c930e9bb0330776b3971c9be2c246eb9e2c6e6b089daf6982191db7"], algorithm=secrets["ALGORITHM"])
