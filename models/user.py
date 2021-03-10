from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError, validator


class applicant_user(BaseModel):
    
    email: EmailStr

        
class user_to_register(applicant_user):
    name: str = None
    last_name: str = None
    sex: str = None
    phone_numbre: str = None
    institution: str = None
    institution_afiliation: str = None
    profession: str = None
    date_of_birth: str = None
    is_active: Optional[bool] = True
    password: Optional[str] = None
    verify_password: Optional[str] = None

    @validator('verify_password')
    def password_match(cls, password_to_verify, values, **kwargs):
        """ Validate that the value taken by password and verify_password match

        Parameters
        ----------
        cls
            takes user_to_register class as an argument
        password_to_verify: str 
            is the value in the verify_password field 
        values: str
            is the value in the password field, by default the decorator takes 
            this name as a parameter
        **kwargs:  
            if provided, this will include the arguments above not explicitly 
            listed in the signature, this is necessary for the function takes 
            the key value pairs defined in the class

        Return:
        ----------
        password_to_verify: str
            If the password and verify_password match, returns the value in passowrd filed
        
        Raises:
        ----------
        ValueError
            If the password and verify_passowrd does'nt match

        """
        if 'password' in values and password_to_verify != values['password']:
            raise ValueError('passwords do not match')
        return password_to_verify