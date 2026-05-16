import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import SensorStatus, SensorType


class Sensor(TimestampMixin, Base):
    __tablename__ = "sensors"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farm_zones.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    sensor_type: Mapped[SensorType] = mapped_column(Enum(SensorType), default=SensorType.MULTI)
    status: Mapped[SensorStatus] = mapped_column(Enum(SensorStatus), default=SensorStatus.ONLINE)
    hardware_id: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    firmware_version: Mapped[str | None] = mapped_column(String(40))
    battery_level: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=100)
    signal_strength: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=100)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    farm: Mapped["Farm"] = relationship(back_populates="sensors")
    zone: Mapped["FarmZone | None"] = relationship(back_populates="sensors")
    readings: Mapped[list["SensorReading"]] = relationship(back_populates="sensor", cascade="all, delete-orphan")


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    __table_args__ = (
        Index("ix_sensor_readings_farm_recorded_at", "farm_id", "recorded_at"),
        Index("ix_sensor_readings_zone_recorded_at", "zone_id", "recorded_at"),
        Index("ix_sensor_readings_sensor_recorded_at", "sensor_id", "recorded_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    sensor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sensors.id", ondelete="CASCADE"), index=True)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farm_zones.id", ondelete="SET NULL"), index=True)
    soil_moisture: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    temperature: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    humidity: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    water_tank_level: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    ph_level: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))
    rainfall_mm: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    nitrogen: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    phosphorus: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    potassium: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    light_intensity: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    wind_speed: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))
    anomaly_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 3))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    sensor: Mapped[Sensor] = relationship(back_populates="readings")
    farm: Mapped["Farm"] = relationship(back_populates="readings")
    zone: Mapped["FarmZone | None"] = relationship(back_populates="readings")
