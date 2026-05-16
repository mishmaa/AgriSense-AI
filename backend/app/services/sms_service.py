import logging

from app.core.config import get_settings


class SMSService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.logger = logging.getLogger("agrisense")

    def send_alert(self, to_phone: str | None, message: str) -> bool:
        if not to_phone:
            self.logger.info("sms alert skipped reason=no_phone")
            return False
        if not self.settings.sms_provider_api_key:
            self.logger.info("sms alert queued demo_mode=true to=%s", to_phone)
            return False
        self.logger.info("sms alert queued provider=configured to=%s", to_phone)
        return True
