import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import JSONType
from app.models.enums import MissionStatus


class DroneMission(Base):
    __tablename__ = "drone_missions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    mission_name: Mapped[str] = mapped_column(String(160))
    status: Mapped[MissionStatus] = mapped_column(Enum(MissionStatus), default=MissionStatus.PLANNED)
    flight_path: Mapped[dict] = mapped_column(JSONType, default=dict)
    imagery_url: Mapped[str | None] = mapped_column(String(500))
    ai_findings: Mapped[dict] = mapped_column(JSONType, default=dict)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
