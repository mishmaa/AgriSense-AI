import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import SensorStatus, SensorType
from app.schemas.common import ORMModel


class SensorCreate(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    name: str = Field(min_length=2, max_length=120)
    sensor_type: SensorType = SensorType.MULTI
    hardware_id: str = Field(min_length=2, max_length=120)
    firmware_version: str | None = Field(default=None, max_length=40)


class SensorRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None
    name: str
    sensor_type: SensorType
    status: SensorStatus
    hardware_id: str
    firmware_version: str | None
    battery_level: Decimal
    signal_strength: Decimal
    last_seen_at: datetime | None
    created_at: datetime


class SensorReadingCreate(BaseModel):
    sensor_id: uuid.UUID
    soil_moisture: Decimal | None = Field(default=None, ge=0, le=100)
    temperature: Decimal | None = Field(default=None, ge=-30, le=70)
    humidity: Decimal | None = Field(default=None, ge=0, le=100)
    water_tank_level: Decimal | None = Field(default=None, ge=0, le=100)
    ph_level: Decimal | None = Field(default=None, ge=0, le=14)
    rainfall_mm: Decimal | None = Field(default=None, ge=0)
    nitrogen: Decimal | None = Field(default=None, ge=0)
    phosphorus: Decimal | None = Field(default=None, ge=0)
    potassium: Decimal | None = Field(default=None, ge=0)
    light_intensity: Decimal | None = Field(default=None, ge=0)
    wind_speed: Decimal | None = Field(default=None, ge=0)
    anomaly_score: Decimal | None = Field(default=None, ge=0, le=1)
    recorded_at: datetime | None = None


class SensorReadingBatchCreate(BaseModel):
    readings: list[SensorReadingCreate] = Field(min_length=1, max_length=500)


class SensorReadingRead(ORMModel):
    id: uuid.UUID
    sensor_id: uuid.UUID
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None
    soil_moisture: Decimal | None
    temperature: Decimal | None
    humidity: Decimal | None
    water_tank_level: Decimal | None
    ph_level: Decimal | None
    rainfall_mm: Decimal | None
    nitrogen: Decimal | None
    phosphorus: Decimal | None
    potassium: Decimal | None
    light_intensity: Decimal | None
    wind_speed: Decimal | None
    anomaly_score: Decimal | None
    recorded_at: datetime
