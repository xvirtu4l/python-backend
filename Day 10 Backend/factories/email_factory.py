from config.settings import get_settings
from services.email_service import EmailService


def get_email_service() -> EmailService:
    settings = get_settings()
    return EmailService(
        smtp_host=settings.email.smtp_host,
        smtp_port=settings.email.smtp_port,
        smtp_username=settings.email.smtp_username,
        smtp_password=settings.email.smtp_password,
        from_email=settings.email.from_email,
        from_name=settings.email.from_name,
        use_tls=settings.email.use_tls,
        use_ssl=settings.email.use_ssl,
    )
