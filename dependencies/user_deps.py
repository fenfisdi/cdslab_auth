from jose import jwt
from dotenv import dotenv_values

from models import user

secrets = dotenv_values(".secrets")

def tokinize_email(cls: user.applicant_user, email: str) -> str:



