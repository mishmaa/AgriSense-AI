from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.weather import WeatherSnapshot
from app.schemas.weather import WeatherSnapshotCreate, WeatherSnapshotRead
from app.services.farm_service import FarmService
from app.services.weather_service import WeatherService


router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/farm/{farm_id}", response_model=list[WeatherSnapshotRead])
def latest_weather(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[WeatherSnapshot]:
    FarmService(db).get_for_user(farm_id, current_user)
    return WeatherService(db).latest_for_farm(farm_id)


@router.post("/snapshot", response_model=WeatherSnapshotRead, status_code=status.HTTP_201_CREATED)
def create_weather_snapshot(
    payload: WeatherSnapshotCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> WeatherSnapshot:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return WeatherService(db).create_snapshot(payload)
