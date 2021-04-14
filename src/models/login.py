from pydantic import BaseModel, validator, Field, EmailStr

from src.utils import Security


class LoginUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    @validator('password', pre=True)
    def set_hash(cls, value: str):
        value = Security.hash_password(value)
        return value


class RecoverUser(BaseModel):
    password: str = Field(...)
    verify_password: str = Field(...)

    @validator('password')
    def password_match(cls, value, values):
        if value != values.get('verify_password'):
            raise ValueError("Provided passwords don't match")
        return value


class OTPUser(BaseModel):
    email: EmailStr = Field(...)
    otp_code: str = Field(...)
