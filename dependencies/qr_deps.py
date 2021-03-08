import pyotp
import qrcode

from PIL import Image

from models.qr import qr
from models.user import applicant_user


def generate_key_qr() -> qr.qr_key:

    return pyotp.random_base32()

def generate_qr_url(key: qr.qr_key, email: applicant_user.email) -> qr.qr_url:

    return pyotp.TOTP(key).prvisioning_uri(email)

def generate_qr_img(url: qr.qr_url, email: applicant_user.email) -> qr.qr_img:

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

