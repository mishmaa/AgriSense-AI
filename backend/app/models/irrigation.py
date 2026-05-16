import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import IrrigationMode, IrrigationStatus


class IrrigationEvent(Base):
    __tablename__ = "irrigation_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farm_zones.id", ondelete="SET NULL"), index=True)
    triggered_by_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    mode: Mapped[IrrigationMode] = mapped_column(Enum(IrrigationMode), default=IrrigationMode.MANUAL)
    status: Mapped[IrrigationStatus] = mapped_column(Enum(IrrigationStatus), default=IrrigationStatus.STARTED)
    water_used_liters: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    reason: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    farm: Mapped["Farm"] = relationship(back_populates="irrigation_events")
