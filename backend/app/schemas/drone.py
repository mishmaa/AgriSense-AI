import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import MissionStatus
from app.schemas.common import ORMModel


class DroneMissionCreate(BaseModel):
    farm_id: uuid.UUID
    mission_name: str = Field(min_length=2, max_length=160)
    flight_path: dict[str, Any] = Field(default_factory=dict)
    scheduled_at: datetime | None = None


class DroneMissionRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    created_by_id: uuid.UUID
    mission_name: str
    status: MissionStatus
    flight_path: dict[str, Any]
    imagery_url: str | None
    ai_findings: dict[str, Any]
    scheduled_at: datetime | None
    completed_at: datetime | None
