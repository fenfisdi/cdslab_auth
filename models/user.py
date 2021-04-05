from datetime import datetime
from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, Field, constr
from dotenv import dotenv_values

from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)
from dependencies import responses
from pprint import pprint

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class user_to_register(BaseModel):
    email: EmailStr


class security_questions(BaseModel):

    questions: list
    answers: list


class user_to_register(user_email):
    name: str = Field(max_length=64, strip_whitespace=True)
    last_name: str = Field(max_length=63, strip_whitespace=True)
    sex: str = Field(max_length=1)
    phone_number: constr(max_length=50, strip_whitespace=True)
    institution: str = Field(max_length=63)
    institution_afiliation: str = Field(min_length=3)
    profession: str = Field(min_length=3)
    date_of_birth: datetime
    security_questions: security_questions

    @validator('name', 'last_name', 'institution', 'institution_afiliation', 'profession')
    def validate_alphabetic_field(cls, alphabetic_field, **kwargs):
        """
        Validates if the name, last_name, institution, institution_afiliation and profession fields
        contains only alphabetic characters

        Parameters
        ----------
        cls: Pydantic class refers to user_to_register
                Inherits the pydantic BaseModel class
        alphabetic_field: Field
                The fields that must contains only alphabetic characters

        Return
        ----------
        alphabetic_field: str
            If the field just contains alphabetic characters, returns de value of this string
        assert: str
            If the field doesn't contain alphabetic characters

        """
        if alphabetic_field.isalpha():
            return alphabetic_field
        return responses.error_response_model(f'{kwargs["field"].name} ''must be alphabetic', 404, 'Error')

    @ validator('sex')
    def validate_sex(cls, sex):
        """
        Validates if the field sex is the letter M or F

        Parameters
        ----------
        cls: Pydantic class refers to user_to_register
                Inherits the pydantic BaseModel class
        sex: Field
                The sex entered by the user in the registration step

        Return
        ----------
        sex: str
            If the field just contains alphabetic characters, returns de value of this string

        Raise
        ----------
        ValueError: str
            If the field isn't F or M letters

        """
        if sex != "M" and sex != "F":
            return responses.error_response_model("sex field must be M or F letter", 404, "Error")
        return sex

    @ validator('phone_number')
    def validate_phone_number(cls, phone_number):
        """
        Validates if the field is a valid phone number. the phone number must contains:
        the plus symbol '+', the country code,  local code and 7 digits.

        Parameters
        ----------
        cls: Pydantic class refers to user_to_register
                Inherits the pydantic BaseModel class
        phone_number: constr
                The phone number entered by the user in the registration step

        Return
        ----------
        phone_number: str
            If the field is a valid phone_number

        Raise
        ----------
        ValueError: str
            If the field is a invalid phone number or invalid mobile number

        """
        if phone_number is None:
            return phone_number
        try:
            n = parse_phone_number(phone_number, 'GB')
        except NumberParseException as e:
            return responses.error_response_model('phone_number please provide a valid phone number', 404, 'Error')

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            return responses.error_response_model(
                'phone_number: please provide a valid phone number', 404, 'Error')

        return format_number(n, PhoneNumberFormat.NATIONAL if n.country_code == 44 else PhoneNumberFormat.INTERNATIONAL)


class user_in(user_to_register):
    password: Optional[str] = None
    verify_password: Optional[str] = None

    @ validator('verify_password')
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
            return responses.error_response_model(
                'password: password doesn´t match with verify', 404, 'Password Error')
        return password_to_verify


class user_in_db(user_to_register):

    is_active: bool = False
    rol: str = "regular"
    hashed_password: Optional[str] = None
    key_qr: Optional[str] = None


class auth_in(BaseModel):
    email: EmailStr
    password: str


class two_auth_in(BaseModel):
    email: EmailStr
    qr_value: str


class auth_refresh(BaseModel):
    email: EmailStr
    key_qr: str


class recover_password(user_email):

    new_password: Optional[str] = None
    new_verify_password: Optional[str] = None

    @validator('new_verify_password')
    def password_match(cls, new_password_to_verify, values):
        """
            Validates whether passwords provided match

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            password_to_verify: str
                User's input with the password to check

            values: dict
                Dictionary containing the stored password to compare

            Return
            ----------
            password_to_verify: str
                If the field passes the validation,
                this string is returned back

            Raises
            ----------
            ValueError
                If the field doesn't pass the validation
        """
        if 'new_password' in values and new_password_to_verify != values['new_password']:
            return responses.error_response_model(
                'password: password doesn´t match with verify', 404, 'Password Error')
        return new_password_to_verify


class enter_responses(user_email):

    answers = list()
