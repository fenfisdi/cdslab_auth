import jsoncfg
import pyotp

from PIL import Image
from operations.user_operations import retrieve_user
from dependencies import qr_deps

from models.user import user_to_register

qr_settings = jsoncfg.load_config('qr.cfg')


def generate_key_qr() -> str:
    """
    Generates a random key that will be use to generate the QR code with an email asociated

    Returns
    ----------
    pyotp.random_base32 : str

    """
    return pyotp.random_base32()


def generate_url_qr(qr_key: str, user: user_to_register) -> str:
    """
    Generates the url that contains the QR associated with the user email, this
    QR can be rendered by the frontend

    Parameters
    ----------
    qr_key: str
            A str generated by the pyotp library

    user: Pydantic class
           inherits the properties of user_to_register


    Returns
    ----------
    url_qr: Url
            A URL generated by the key_qr and the email user associated
    """
    url_qr = pyotp.TOTP(qr_key).provisioning_uri(user.email)
    return url_qr


def get_value_key_qr(key_qr: str):
    """
    Get value that the user see when read the QR code with Google Authenticator

    Parameters
    ----------
    key_qr: str
            String obtained by the client



    Returns
    ----------
    value: Url
            A URL generated by the key_qr and the email user associated
    """
    return pyotp.TOTP(key_qr).now()


def validate_qr(query: dict, qr_value: str):
    """
    Validate key qr by user and value

    Parameters
    ----------
    query: dict
            Database search query 

    qr_value:str
            Value to compare

    Returns
    ----------
    value: Boolean

    """
    user_retrieve = retrieve_user(query)
    if user_retrieve:
        key_qr_value = qr_deps.get_value_key_qr(user_retrieve["key_qr"])
        if key_qr_value:
            if str(key_qr_value) == str(qr_value):
                return True
            return False
        return False
    return False
