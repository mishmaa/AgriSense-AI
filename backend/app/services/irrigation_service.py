from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.enums import IrrigationStatus
from app.models.irrigation import IrrigationEvent
from app.models.user import User
from app.schemas.irrigation import IrrigationStartRequest, IrrigationStopRequest


class IrrigationService:
    def __init__(self, db: Session):
        self.db = db

    def start(self, payload: IrrigationStartRequest, user: User) -> IrrigationEvent:
        event = IrrigationEvent(
            farm_id=payload.farm_id,
            zone_id=payload.zone_id,
            triggered_by_id=user.id,
            mode=payload.mode,
            status=IrrigationStatus.STARTED,
            reason=payload.reason,
            started_at=datetime.now(UTC),
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def stop(self, payload: IrrigationStopRequest) -> IrrigationEvent:
        event = self.db.get(IrrigationEvent, payload.event_id)
        if not event:
            raise NotFoundError("Irrigation event not found.")
        event.status = IrrigationStatus.COMPLETED
        event.ended_at = datetime.now(UTC)
        event.water_used_liters = payload.water_used_liters
        self.db.commit()
        self.db.refresh(event)
        return event

    def history(self, farm_id: UUID, limit: int = 100) -> list[IrrigationEvent]:
        query = (
            select(IrrigationEvent)
            .where(IrrigationEvent.farm_id == farm_id)
            .order_by(desc(IrrigationEvent.started_at))
            .limit(limit)
        )
        return list(self.db.scalars(query))
