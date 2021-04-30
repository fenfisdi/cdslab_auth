from pydantic import BaseModel, validator, Field, EmailStr

from src.utils.security import Security


class LoginUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    @validator('password', pre=True)
    def set_hash(cls, value: str):
        value = Security.hash_password(value)
        return value


class RecoverUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    verify_password: str = Field(...)

    @validator('verify_password')
    def password_match(cls, value, values):
        if value != values.get('password'):
            raise ValueError("Provided passwords don't match")
        return value

    @validator('password', 'verify_password', pre=True)
    def set_hash(cls, value: str):
        value = Security.hash_password(value)
        return value


class SecurityCode(BaseModel):
    email: EmailStr = Field(...)
    security_code: str = Field(...)


class OTPUser(BaseModel):
    email: EmailStr = Field(...)
    otp_code: str = Field(...)
