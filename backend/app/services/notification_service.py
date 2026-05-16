from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationCreate
from app.models.enums import NotificationChannel
from app.services.email_service import EmailService
from app.services.sms_service import SMSService


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: NotificationCreate) -> Notification:
        notification = Notification(
            user_id=payload.user_id,
            farm_id=payload.farm_id,
            notification_type=payload.notification_type,
            channel=payload.channel,
            severity=payload.severity,
            title=payload.title,
            message=payload.message,
            metadata_json=payload.metadata,
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        self._dispatch(notification)
        return notification

    def list_for_user(self, user: User, limit: int = 100) -> list[Notification]:
        query = (
            select(Notification)
            .where(Notification.user_id == user.id)
            .order_by(desc(Notification.created_at))
            .limit(limit)
        )
        return list(self.db.scalars(query))

    def mark_read(self, notification_id: UUID, user: User) -> Notification:
        notification = self.db.get(Notification, notification_id)
        if not notification or notification.user_id != user.id:
            raise NotFoundError("Notification not found.")
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def _dispatch(self, notification: Notification) -> None:
        user = self.db.get(User, notification.user_id)
        if not user:
            return
        if notification.channel == NotificationChannel.EMAIL:
            EmailService().send_alert(user.email, notification.title, notification.message)
        if notification.channel == NotificationChannel.SMS:
            SMSService().send_alert(user.phone, notification.message)
