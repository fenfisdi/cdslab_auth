from os import environ

from src.services import ManagementAPI


class SendEmailVerificationUseCase:

    @classmethod
    def handle(cls, email: str, token: str):
        message = cls.create_url_message(token)
        data = {
            "email": email,
            "subject": "Validation Account",
            "message": message,
        }
        _, _ = ManagementAPI.send_email(data)

    @classmethod
    def create_url_message(cls, token: str) -> str:
        url = environ.get('FENFISDI_HOST', '') + '/auth'
        endpoint = f'/register/user/email?token={token}'

        magick_url = "".join([url, endpoint])

        template = f'<a href="{magick_url}">Verify Mail</a>'
        return template


class SendCodeVerificationUseCase:
    @classmethod
    def handle(cls, email: str, otp_code: str):
        data = {
            "email": email,
            "subject": "Verification Code",
            "message": f"Su codigo de Verificación es: {otp_code}",
        }
        _, _ = ManagementAPI.send_email(data)
