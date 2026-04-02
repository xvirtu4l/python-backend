from config.settings import get_settings
from services.email_service import EmailService


def get_email_service() -> EmailService:
    settings = get_settings()
    return EmailService(
        provider=settings.email.provider,
        sendgrid_api_key=settings.email.sendgrid_api_key,
        from_email=settings.email.from_email,
        from_name=settings.email.from_name,
    )
