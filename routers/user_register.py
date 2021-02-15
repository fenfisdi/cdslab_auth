import sys
sys.path.append('./')
from pydantic import BaseModel, ValidationError, validator
from fastapi import Form, FastAPI, Request, HTTPException, Depends

from config import config

class user_base(BaseModel):
    
    name: str = None
    last_name: str = None
    email: str = None
    sex: str = None
    phone_numbre: str = None
    institution: str = None
    institution_afiliation: str = None
    profession: str = None
    date_of_birth: str = None

    @validator('email')
    def email_validation(cls, v):
        for validator in config.email_name_validators():
            if validator not in v:
                raise  ValueError('invalid email')
        return v
    
app = FastAPI()


@app.get()


    