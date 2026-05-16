import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import Severity
from app.schemas.common import ORMModel


class WeatherSnapshotCreate(BaseModel):
    farm_id: uuid.UUID
    temperature: Decimal
    humidity: Decimal = Field(ge=0, le=100)
    rainfall_mm: Decimal = Field(default=0, ge=0)
    wind_speed: Decimal = Field(default=0, ge=0)
    condition: str
    risk_level: Severity = Severity.LOW
    captured_at: datetime | None = None


class WeatherSnapshotRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    temperature: Decimal
    humidity: Decimal
    rainfall_mm: Decimal
    wind_speed: Decimal
    condition: str
    risk_level: Severity
    captured_at: datetime
