from datetime import datetime
from typing import Optional, List

from phonenumbers import (
    NumberParseException, PhoneNumberFormat, PhoneNumberType,
    format_number, is_valid_number, number_type,
    parse as parse_phone_number
)
from pydantic import BaseModel, EmailStr, validator, Field, constr

from src.config import settings

MOBILE_NUMBER_TYPES = \
    PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class user_email(BaseModel):
    email: EmailStr


class SecurityQuestion(BaseModel):
    question: list
    answer: list


class enter_responses(user_email):
    security_code: str


class UserInput(BaseModel):
    name: str = Field(..., max_length=64, regex='[a-zA-Z]')
    last_name: str = Field(..., max_length=64)
    email: EmailStr = Field(...)
    phone_number: str = Field(...)
    institution: str = Field(..., max_length=64)
    institution_afiliation: str = Field(..., min_length=3)
    profession: str = Field(None, min_length=3)
    gender: str = Field(None, max_length=1)

    date_of_birth: datetime
    security_questions: List[SecurityQuestion]


class BaseUser(BaseModel):
    email: EmailStr
    name: str = Field(..., max_length=64, regex='[a-zA-Z]')
    last_name: str = Field(..., max_length=64)
    institution: str = Field(..., max_length=64)
    institution_afiliation: str = Field(..., min_length=3)
    profession: str = Field(None, min_length=3)
    gender: str = Field(None, max_length=1)
    phone_number: constr(max_length=50, strip_whitespace=True)
    date_of_birth: datetime
    security_questions: List[SecurityQuestion]

    @validator('name', 'last_name', 'institution',
               'institution_afiliation', 'profession')
    def validate_alphabetic_field(cls, alphabetic_field):
        """
            Validates that the `alphabetic_field` contains only alphabetic
            characters

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            alphabetic_field: str
                String which must contain only alphabetic characters

            Return
            ----------
            alphabetic_field: str
                If the field passes the validation,
                this string is returned back

            Raises
            ----------
            AssertionError
                If the field doesn't pass the validation
        """
        # TODO: Verify return, is response or exception?
        if alphabetic_field.isalpha():
            return alphabetic_field
        return "Any Error"
        #return responses.error_response_model(f'{kwargs["field"].name} ''must be alphabetic', 404, 'Error')

    @validator('gender')
    def validate_sex(cls, value):
        """
            Validates that `sex` field is either M or F

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            value: str
                It must be either M or F

            Return
            ----------
            sex: str
                If the field passes the validation,
                this string is returned back

            Raises
            ----------
            ValueError
                If the field doesn't pass the validation
        """
        if value != 'M' and value != 'F':
            raise ValueError('Invalid type')
        return value
    #
    #     # TODO VERIFY ANSEWERS
    #     # if sex != "M" and sex != "F":
    #     #     return responses.error_response_model("sex field must be M or F letter", 404, "Error")
    #     # return sex
    #
    @validator('phone_number')
    def validate_phone_number(cls, phone_number):
        """
            Validates `phone_number` to contain `+` sign, country code,
            local code and 7 digits.

            Also validates that `phone_number` is not None.

            Parameters
            ----------
            cls: Pydantic class extended from BaseModel

            phone_number: str
                Phone number entered by the user

            Return
            ----------
            phone_number: str
                If the field passes the validation,
                this string is returned back

            Raises
            ----------
            ValueError
                If the field doesn't pass the validation
        """
        if phone_number is None:
            raise ValueError('Phone number cannot be empty')

        try:
            phone_number_object = parse_phone_number(
                phone_number,
                region=settings['REGION_CODE']
                )
        except NumberParseException as error:
            raise ValueError(
                'Please provide a valid phone number') from error

        if not is_valid_number(phone_number_object):
            raise ValueError('Please provide a valid phone number')

        if number_type(phone_number_object) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid phone number')

        if phone_number_object.country_code == settings['COUNTRY_CODE']:
            phone_nationality = PhoneNumberFormat.NATIONAL
        else:
            phone_nationality = PhoneNumberFormat.INTERNATIONAL

        return format_number(phone_number_object, phone_nationality)

    # #TODO: Check logic and responses
    #
    # # if phone_number is None:
    # #     return phone_number
    # # try:
    # #     n = parse_phone_number(phone_number, 'GB')
    # # except NumberParseException as e:
    # #     return responses.error_response_model(
    # #         'phone_number please provide a valid phone number', 404, 'Error')
    # #
    # # if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
    # #     return responses.error_response_model(
    # #         'phone_number: please provide a valid phone number', 404, 'Error')
    # #
    # # return format_number(n,
    # #                      PhoneNumberFormat.NATIONAL if n.country_code == 44 else PhoneNumberFormat.INTERNATIONAL)


class User(BaseUser):
    password: Optional[str] = None
    verify_password: Optional[str] = None

    @validator('verify_password')
    def password_match(cls, password_to_verify, values):
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
        if 'password' in values and password_to_verify != values['password']:
            raise ValueError("Provided passwords don't match")
        return password_to_verify

        # TODO: Check response

        # if 'password' in values and password_to_verify != values['password']:
        #     return responses.error_response_model(
        #         'password: password doesn´t match with verify', 404, 'Password Error')
        # return password_to_verify

class StoredUser(BaseUser):
    is_active: bool = False
    role: str = 'regular'
    hashed_password: Optional[str] = None
    key_qr: Optional[str] = None


class PreAuthenticatedUser(BaseModel):
    email: EmailStr
    password: str


class AuthenticatedUser(BaseModel):
    email: EmailStr
    qr_value: str


class RecoverUser(user_email):
    new_password: Optional[str] = None
    new_verify_password: Optional[str] = None

    # TODO: Verify Validator
    @validator('new_verify_password')
    def password_match(cls, new_password_to_verify, values):
        if 'new_password' in values and new_password_to_verify != values[
            'new_password']:
            return 'Any'
            # return responses.error_response_model(
            #     'password: password doesn´t match with verify', 404,
            #     'Password Error')
        return new_password_to_verify


class SecurityCode(user_email):
    security_code: str
