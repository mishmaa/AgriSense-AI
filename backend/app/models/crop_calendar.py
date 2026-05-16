import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import CalendarActivityType, CalendarStatus


class CropCalendarEvent(Base):
    __tablename__ = "crop_calendar_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farm_zones.id", ondelete="SET NULL"), index=True)
    crop_name: Mapped[str] = mapped_column(String(120))
    activity_type: Mapped[CalendarActivityType] = mapped_column(Enum(CalendarActivityType), index=True)
    title: Mapped[str] = mapped_column(String(180))
    notes: Mapped[str | None] = mapped_column(Text)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[CalendarStatus] = mapped_column(Enum(CalendarStatus), default=CalendarStatus.PENDING)
