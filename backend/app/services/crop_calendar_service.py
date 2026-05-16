from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.crop_calendar import CropCalendarEvent
from app.models.enums import CalendarStatus
from app.schemas.crop_calendar import CropCalendarEventCreate, CropCalendarEventUpdate


class CropCalendarService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: CropCalendarEventCreate) -> CropCalendarEvent:
        event = CropCalendarEvent(**payload.model_dump())
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def list_for_farm(self, farm_id: UUID) -> list[CropCalendarEvent]:
        query = select(CropCalendarEvent).where(CropCalendarEvent.farm_id == farm_id).order_by(
            CropCalendarEvent.scheduled_for
        )
        return list(self.db.scalars(query))

    def update(self, event_id: UUID, payload: CropCalendarEventUpdate) -> CropCalendarEvent:
        event = self.db.get(CropCalendarEvent, event_id)
        if not event:
            raise NotFoundError("Crop calendar event not found.")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(event, key, value)
        if event.status == CalendarStatus.COMPLETED and event.completed_at is None:
            event.completed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(event)
        return event
