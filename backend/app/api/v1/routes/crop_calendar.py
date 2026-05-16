from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.models.crop_calendar import CropCalendarEvent
from app.models.user import User
from app.schemas.crop_calendar import CropCalendarEventCreate, CropCalendarEventRead, CropCalendarEventUpdate
from app.services.crop_calendar_service import CropCalendarService
from app.services.farm_service import FarmService


router = APIRouter(prefix="/crop-calendar", tags=["Crop Calendar"])


@router.get("/farm/{farm_id}", response_model=list[CropCalendarEventRead])
def list_events(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CropCalendarEvent]:
    FarmService(db).get_for_user(farm_id, current_user)
    return CropCalendarService(db).list_for_farm(farm_id)


@router.post("/", response_model=CropCalendarEventRead, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: CropCalendarEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CropCalendarEvent:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return CropCalendarService(db).create(payload)


@router.patch("/{event_id}", response_model=CropCalendarEventRead)
def update_event(
    event_id: UUID,
    payload: CropCalendarEventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CropCalendarEvent:
    event = db.get(CropCalendarEvent, event_id)
    if not event:
        raise NotFoundError("Crop calendar event not found.")
    FarmService(db).get_for_user(event.farm_id, current_user)
    return CropCalendarService(db).update(event_id, payload)
