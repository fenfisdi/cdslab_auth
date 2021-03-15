from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationError, validator, Field, constr, PositiveInt
from datetime import date, datetime
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)


MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE

class user_to_register(BaseModel):
    email: EmailStr
    name: str = Field(max_length=64, strip_whitespace=True)
    last_name: str = Field(max_length=63, strip_whitespace=True)
    sex: str = Field(max_length=1)
    phone_number: constr(max_length=50, strip_whitespace=True)
    institution: str = Field(max_length=63)
    institution_afiliation: str = Field(min_length=3)
    profession: str = Field(min_length=3)
    date_of_birth: datetime

    @validator('name', 'last_name', 'institution', 'institution_afiliation', 'profession')
    def validate_alphabetic_field(cls, alphabetic_field):
        """Valid that the value entered by the user in the registration step is an alphabetic string

        Keywords arguments:
        cls -- takes user_to_register class as an argument
        alphabetic_field -- takes the value of decorator and applies the function, in this case name, 
        Last_name, institution, institution_afiliation, profession.
        """
        assert alphabetic_field.isalpha(), "must be alphabetic field"
        return alphabetic_field

    @validator('sex')
    def validate_sex(cls, sex):
        """Valid that the field sex take just the value M or f

        Keywords arguments:
        cls -- takes user_to_register class as an argument
        sex -- takes the value of decorator and applies the function
        """
        if sex != "M" and sex != "F":
            raise ValueError("Invalid type")
        return sex

    @validator('phone_number')
    def validate_phone_number(cls, phone_number):
        if phone_number is None:
            return phone_number
        try:
            n = parse_phone_number(phone_number, 'GB')
        except NumberParseException as e:
            raise ValueError(
                'Please provide a valid mobile phone number') from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(n, PhoneNumberFormat.NATIONAL if n.country_code == 44 else PhoneNumberFormat.INTERNATIONAL)


class user_in(user_to_register):
    password: str = None
    verify_password: str = None

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


class user_in_db(user_to_register):

    is_active: bool = False
    rol: str = "regular"
    hashed_password: str = None
    key_qr: str = None


class auth_in(BaseModel):
    email: EmailStr
    password: str

class two_auth_in(BaseModel):
    email: EmailStr
    qr_value: str