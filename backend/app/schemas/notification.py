import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import NotificationChannel, NotificationSeverity, NotificationType
from app.schemas.common import ORMModel


class NotificationCreate(BaseModel):
    user_id: uuid.UUID
    farm_id: uuid.UUID | None = None
    notification_type: NotificationType
    channel: NotificationChannel = NotificationChannel.IN_APP
    severity: NotificationSeverity = NotificationSeverity.INFO
    title: str = Field(min_length=2, max_length=180)
    message: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class NotificationRead(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID
    farm_id: uuid.UUID | None
    notification_type: NotificationType
    channel: NotificationChannel
    severity: NotificationSeverity
    title: str
    message: str
    metadata_json: dict[str, Any]
    is_read: bool
    created_at: datetime
