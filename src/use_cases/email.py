from src.services import ManagementAPI


class SendEmailVerificationUseCase:

    @classmethod
    def handle(cls, email: str, token: str):
        data = {
            "email": email,
            "subject": "Validation Account",
            "message": token,
        }
        _, _ = ManagementAPI.send_email(data)


class SendCodeVerificationUseCase:
    @classmethod
    def handle(cls, email: str, otp_code: str):
        data = {
            "email": email,
            "subject": "Verification Code",
            "message": f"Su codigo de Verificación es: {otp_code}",
        }
        _, _ = ManagementAPI.send_email(data)
