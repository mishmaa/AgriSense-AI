import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import Severity


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    temperature: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    humidity: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    rainfall_mm: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=0)
    wind_speed: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=0)
    condition: Mapped[str] = mapped_column(String(120))
    risk_level: Mapped[Severity] = mapped_column(Enum(Severity), default=Severity.LOW)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
