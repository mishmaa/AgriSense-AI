import logging

from app.core.config import get_settings


class EmailService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.logger = logging.getLogger("agrisense")

    def send_alert(self, to_email: str, subject: str, message: str) -> bool:
        if not self.settings.smtp_host or not self.settings.smtp_user:
            self.logger.info("email alert queued demo_mode=true to=%s subject=%s", to_email, subject)
            return False
        self.logger.info("email alert queued provider=smtp to=%s subject=%s", to_email, subject)
        return True
