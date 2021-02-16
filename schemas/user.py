from typing import Optional

from pydantic import BaseModel, EmailStr, ValidationError, validator

#shared properties
class user_base(BaseModel):
    name: str = None
    last_name: str = None
    email: Optional[EmailStr] = None
    sex: str = None
    phone_numbre: str = None
    institution: str = None
    institution_afiliation: str = None
    profession: str = None
    date_of_birth: str = None
    is_active: Optional[bool] = True
    
class user_create(user_base):
    email: EmailStr

class user_register(user_base):
    password: Optional[str] = None
    verify_password: Optional[str] = None

    @validator('verify_password')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    


 