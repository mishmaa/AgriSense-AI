import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import CalendarActivityType, CalendarStatus
from app.schemas.common import ORMModel


class CropCalendarEventCreate(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    crop_name: str = Field(min_length=2, max_length=120)
    activity_type: CalendarActivityType
    title: str = Field(min_length=2, max_length=180)
    notes: str | None = None
    scheduled_for: datetime


class CropCalendarEventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    notes: str | None = None
    scheduled_for: datetime | None = None
    completed_at: datetime | None = None
    status: CalendarStatus | None = None


class CropCalendarEventRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None
    crop_name: str
    activity_type: CalendarActivityType
    title: str
    notes: str | None
    scheduled_for: datetime
    completed_at: datetime | None
    status: CalendarStatus
