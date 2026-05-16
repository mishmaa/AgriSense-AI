import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import IrrigationMode


class Farm(TimestampMixin, Base):
    __tablename__ = "farms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    location_name: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7))
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7))
    total_area_hectares: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    soil_type: Mapped[str] = mapped_column(String(80))
    water_source: Mapped[str | None] = mapped_column(String(120))

    owner: Mapped["User"] = relationship(back_populates="farms")
    zones: Mapped[list["FarmZone"]] = relationship(back_populates="farm", cascade="all, delete-orphan")
    sensors: Mapped[list["Sensor"]] = relationship(back_populates="farm", cascade="all, delete-orphan")
    readings: Mapped[list["SensorReading"]] = relationship(back_populates="farm")
    irrigation_events: Mapped[list["IrrigationEvent"]] = relationship(back_populates="farm")


class FarmZone(TimestampMixin, Base):
    __tablename__ = "farm_zones"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    crop_name: Mapped[str] = mapped_column(String(120))
    area_hectares: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    irrigation_mode: Mapped[IrrigationMode] = mapped_column(Enum(IrrigationMode), default=IrrigationMode.MANUAL)
    moisture_min_threshold: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=35)
    moisture_max_threshold: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=70)

    farm: Mapped[Farm] = relationship(back_populates="zones")
    sensors: Mapped[list["Sensor"]] = relationship(back_populates="zone")
    readings: Mapped[list["SensorReading"]] = relationship(back_populates="zone")
