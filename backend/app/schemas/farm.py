import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import IrrigationMode
from app.schemas.common import ORMModel


class FarmZoneCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    crop_name: str = Field(min_length=2, max_length=120)
    area_hectares: Decimal = Field(gt=0)
    irrigation_mode: IrrigationMode = IrrigationMode.MANUAL
    moisture_min_threshold: Decimal = Field(default=35, ge=0, le=100)
    moisture_max_threshold: Decimal = Field(default=70, ge=0, le=100)


class FarmZoneRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    name: str
    crop_name: str
    area_hectares: Decimal
    irrigation_mode: IrrigationMode
    moisture_min_threshold: Decimal
    moisture_max_threshold: Decimal
    created_at: datetime


class FarmCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    location_name: str = Field(min_length=2, max_length=255)
    latitude: Decimal = Field(ge=-90, le=90)
    longitude: Decimal = Field(ge=-180, le=180)
    total_area_hectares: Decimal = Field(gt=0)
    soil_type: str = Field(min_length=2, max_length=80)
    water_source: str | None = Field(default=None, max_length=120)
    zones: list[FarmZoneCreate] = Field(default_factory=list)


class FarmUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    location_name: str | None = Field(default=None, min_length=2, max_length=255)
    total_area_hectares: Decimal | None = Field(default=None, gt=0)
    soil_type: str | None = Field(default=None, min_length=2, max_length=80)
    water_source: str | None = Field(default=None, max_length=120)


class FarmRead(ORMModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    location_name: str
    latitude: Decimal
    longitude: Decimal
    total_area_hectares: Decimal
    soil_type: str
    water_source: str | None
    created_at: datetime
    updated_at: datetime
    zones: list[FarmZoneRead] = []
