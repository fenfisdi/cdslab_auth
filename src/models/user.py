import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field, validator

from src.utils.security import Security

ALPHANUMERIC = r'^[a-zA-ZñÑ\s]+$'
PHONE_PREFIX = r'^\+[\d]{1,3}$'
FORMAT_DATE = r'^\d{4}-\d{2}-\d{2}$'


class SecurityQuestion(BaseModel):
    question: str = Field(...)
    answer: str = Field(...)


class UpdateUser(BaseModel):
    name: str = Field(None)
    last_name: str = Field(None)
    phone: int = Field(None)
    phone_prefix: str = Field(None)
    institution: str = Field(None)
    institution_role: str = Field(None)
    profession: str = Field(None)
    birthday: datetime = Field(None)
    notify_removal: bool = Field(True)
    notify_simulation_done: bool = Field(True)

    class Config:
        fields = {
            'name': {'max_length': 64, 'regex': ALPHANUMERIC},
            'last_name': {'max_length': 64, 'regex': ALPHANUMERIC},
            'phone_prefix': {'regex': PHONE_PREFIX},
            'institution': {'max_length': 64, 'regex': ALPHANUMERIC},
            'institution_role': {'max_length': 64, 'regex': ALPHANUMERIC},
            'profession': {'max_length': 64, 'regex': ALPHANUMERIC},
            'gender': {'max_length': 1}
        }

    @validator('birthday', pre=True)
    def validate_birthday(cls, value):
        if re.search(FORMAT_DATE, value):
            return value + 'T00:00'
        return value


class NewUser(UpdateUser):
    name: str = Field(...)
    last_name: str = Field(...)
    phone: int = Field(...)
    phone_prefix: str = Field(...)
    institution: str = Field(...)
    institution_role: str = Field(...)
    birthday: datetime = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    security_questions: List[SecurityQuestion] = Field(...)

    @validator('password', pre=True)
    def set_hash(cls, value: str):
        value = Security.hash_password(value)
        return value
