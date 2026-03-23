import smtplib
from email.message import EmailMessage

from domain.exceptions import BusinessError


class EmailService:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        from_email: str,
        from_name: str,
        use_tls: bool = True,
        use_ssl: bool = False,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email
        self.from_name = from_name
        self.use_tls = use_tls
        self.use_ssl = use_ssl

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

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = recipient_email
        message.set_content(plain_text)
        message.add_alternative(html, subtype="html")

        try:
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    self._authenticate_and_send(server, message)
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.ehlo()
                    if self.use_tls:
                        server.starttls()
                        server.ehlo()
                    self._authenticate_and_send(server, message)
        except smtplib.SMTPException as exc:
            raise BusinessError(f"Không thể gửi email đặt lại mật khẩu: {exc}") from exc
        except OSError as exc:
            raise BusinessError(f"Không thể kết nối đến máy chủ email: {exc}") from exc

    def _authenticate_and_send(self, server: smtplib.SMTP, message: EmailMessage) -> None:
        if self.smtp_username:
            server.login(self.smtp_username, self.smtp_password)
        server.send_message(message)

    def _validate_configuration(self) -> None:
        required_values = {
            "SMTP_HOST": self.smtp_host,
            "SMTP_PORT": str(self.smtp_port),
            "SMTP_FROM_EMAIL": self.from_email,
        }

        missing = [name for name, value in required_values.items() if not value]
        if missing:
            raise BusinessError(
                f"Cấu hình email chưa đầy đủ. Thiếu: {', '.join(missing)}"
            )
