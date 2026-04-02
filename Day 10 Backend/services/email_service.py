from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Email, Mail, To

from domain.exceptions import BusinessError


class EmailService:
    def __init__(
        self,
        provider: str,
        sendgrid_api_key: str,
        from_email: str,
        from_name: str,
    ):
        self.provider = provider
        self.sendgrid_api_key = sendgrid_api_key
        self.from_email = from_email
        self.from_name = from_name

    def send_password_reset_email(self, recipient_email: str, reset_link: str) -> None:
        subject = "Reset your Chatbox password"
        plain_text = (
            "We received a request to reset your Chatbox password.\n\n"
            f"Open this link to reset it: {reset_link}\n\n"
            "This link will expire in 15 minutes.\n"
            "If you did not request this change, you can ignore this email."
        )
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #1b1613; line-height: 1.6;">
            <div style="max-width: 560px; margin: 0 auto; padding: 24px;">
              <div style="margin-bottom: 16px; font-size: 12px; letter-spacing: 0.28em; text-transform: uppercase; color: #8d6d53;">
                Chatbox Security
              </div>
              <h1 style="margin: 0 0 16px; font-size: 28px; color: #2a2118;">
                Reset your password
              </h1>
              <p style="margin: 0 0 16px;">
                We received a request to reset your Chatbox password.
              </p>
              <p style="margin: 0 0 24px;">
                This link stays active for 15 minutes. If you did not request this change, you can safely ignore this email.
              </p>
              <a
                href="{reset_link}"
                style="display: inline-block; padding: 14px 22px; border-radius: 14px; background: #bb5a34; color: #fff8ef; text-decoration: none; font-weight: 600;"
              >
                Reset password
              </a>
              <p style="margin: 24px 0 0; font-size: 13px; color: #5f5146; word-break: break-all;">
                If the button does not work, copy and paste this link into your browser:<br />
                {reset_link}
              </p>
            </div>
          </body>
        </html>
        """
        self._send_email(recipient_email, subject, plain_text, html)

    def _send_email(
        self,
        recipient_email: str,
        subject: str,
        plain_text: str,
        html: str,
    ) -> None:
        self._validate_configuration()

        if self.provider != "sendgrid":
            raise BusinessError(f"Email provider not supported: {self.provider}")

        message = Mail(
            from_email=Email(self.from_email, self.from_name),
            to_emails=To(recipient_email),
            subject=subject,
        )
        message.add_content(Content("text/plain", plain_text))
        message.add_content(Content("text/html", html))

        try:
            client = SendGridAPIClient(self.sendgrid_api_key)
            response = client.send(message)
            if response.status_code >= 400:
                raise BusinessError(
                    f"Không thể gửi email đặt lại mật khẩu: SendGrid returned {response.status_code}"
                )
        except BusinessError:
            raise
        except Exception as exc:
            raise BusinessError(
                f"Không thể gửi email đặt lại mật khẩu: {exc}"
            ) from exc

    def _validate_configuration(self) -> None:
        required_values = {
            "SENDGRID_API_KEY": self.sendgrid_api_key,
            "EMAIL_FROM_ADDRESS": self.from_email,
        }

        missing = [name for name, value in required_values.items() if not value]
        if missing:
            raise BusinessError(
                f"Cấu hình email chưa đầy đủ. Thiếu: {', '.join(missing)}"
            )
