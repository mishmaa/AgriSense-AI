import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import IrrigationMode, IrrigationStatus
from app.schemas.common import ORMModel


class IrrigationStartRequest(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    mode: IrrigationMode = IrrigationMode.MANUAL
    reason: str | None = Field(default=None, max_length=1000)


class IrrigationStopRequest(BaseModel):
    event_id: uuid.UUID
    water_used_liters: Decimal = Field(default=0, ge=0)


class IrrigationEventRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None
    triggered_by_id: uuid.UUID | None
    mode: IrrigationMode
    status: IrrigationStatus
    water_used_liters: Decimal
    reason: str | None
    started_at: datetime
    ended_at: datetime | None
