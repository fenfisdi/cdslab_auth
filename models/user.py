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
        """
            Validate name, last_name, institution, institution_afiliation and profession to
            contain only alphabetic characters

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            alphabetic_field: str
                String containing only alphabetic characters

            Return
            ----------
            alphabetic_field: str
                If the field passes the validation, this string string is returned
            assert: str
                Otherwise, force correction
        """
        assert alphabetic_field.isalpha(), "must be alphabetic field"
        return alphabetic_field

    @validator('sex')
    def validate_sex(cls, sex):
        """
            Validate sex field to either M or F

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            sex: str
                M or F

            Return
            ----------
            sex: str
                If the field passes the validation, this string is returned

            Raise
            ----------
            ValueError: str
                Otherwise, raise an error
        """
        if sex != "M" and sex != "F":
            raise ValueError("Invalid type")
        return sex

    @validator('phone_number')
    def validate_phone_number(cls, phone_number):
        """
            Validate phone_number to contain '+' sign, country code, local code and
            7 digits

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            phone_number: str
                Phone number entered by the user

            Return
            ----------
            phone_number: str
                If the field passes the validation, this string is returned

            Raise
            ----------
            ValueError: str
                Otherwise, raise an error
        """
        if phone_number is None:
            return phone_number
        try:
            n = parse_phone_number(phone_number, 'GB')
        except NumberParseException as e:
            raise ValueError(
                'Please provide a valid mobile phone number') from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        if n.country_code == 44:
            phone_nationality = PhoneNumberFormat.NATIONAL
        else:
            phone_nationality = PhoneNumberFormat.INTERNATIONAL

        return format_number(n, phone_nationality)


class user_in(user_to_register):
    password: Optional[str] = None
    verify_password: Optional[str] = None

    @validator('verify_password')
    def password_match(cls, password_to_verify, values):
        """
            Validate whether passwords match

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            password_to_verify: str
                User input with the password to check

            values: dict
                Dictionary containing the stored password to compare

            Return
            ----------
            password_to_verify: str
                If the field passes the validation, this string is returned

            Raises:
            ----------
            ValueError
                Otherwise, raise an error
        """
        if 'password' in values and password_to_verify != values['password']:
            raise ValueError('passwords do not match')
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
