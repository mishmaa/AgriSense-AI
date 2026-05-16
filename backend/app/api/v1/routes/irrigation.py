from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.core.exceptions import NotFoundError
from app.models.irrigation import IrrigationEvent
from app.models.user import User
from app.schemas.irrigation import IrrigationEventRead, IrrigationStartRequest, IrrigationStopRequest
from app.services.farm_service import FarmService
from app.services.irrigation_service import IrrigationService


router = APIRouter(prefix="/irrigation", tags=["Irrigation"])


@router.post("/start", response_model=IrrigationEventRead)
def start_irrigation(
    payload: IrrigationStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> IrrigationEvent:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return IrrigationService(db).start(payload, current_user)


@router.post("/stop", response_model=IrrigationEventRead)
def stop_irrigation(
    payload: IrrigationStopRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> IrrigationEvent:
    event = db.get(IrrigationEvent, payload.event_id)
    if not event:
        raise NotFoundError("Irrigation event not found.")
    FarmService(db).get_for_user(event.farm_id, current_user)
    return IrrigationService(db).stop(payload)


@router.get("/history/{farm_id}", response_model=list[IrrigationEventRead])
def irrigation_history(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[IrrigationEvent]:
    FarmService(db).get_for_user(farm_id, current_user)
    return IrrigationService(db).history(farm_id)
