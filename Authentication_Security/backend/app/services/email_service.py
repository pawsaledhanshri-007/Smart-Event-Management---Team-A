import logging
import smtplib
from email.message import EmailMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


def _send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email through SMTP. If SMTP is not configured, log a local preview."""
    if not settings.SMTP_HOST:
        logger.warning(
            "SMTP is not configured. Development email preview -> to=%s subject=%s body=%s",
            to_email,
            subject,
            body,
        )
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message.set_content(body)

    if settings.SMTP_USE_TLS:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
            server.starttls()
            if settings.SMTP_USERNAME:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)
    else:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
            if settings.SMTP_USERNAME:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(message)

    return True


def send_password_reset_email(email: str, token: str) -> bool:
    link = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"
    return _send_email(
        email,
        "Reset your password",
        (
            "A password reset was requested for your Smart Event Management account.\n\n"
            f"Reset link: {link}\n\n"
            f"This link expires in {settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes. "
            "If you did not request this, you can ignore this email."
        ),
    )


def send_verification_email(email: str, token: str) -> bool:
    link = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={token}"
    return _send_email(
        email,
        "Verify your email",
        (
            "Verify your email for Smart Event Management.\n\n"
            f"Verification link: {link}\n\n"
            f"This link expires in {settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES} minutes."
        ),
    )
