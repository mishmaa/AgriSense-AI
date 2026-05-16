from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.drone import DroneMission
from app.models.user import User
from app.schemas.drone import DroneMissionCreate, DroneMissionRead
from app.services.drone_service import DroneService
from app.services.farm_service import FarmService


router = APIRouter(prefix="/drone", tags=["Drone Monitoring"])


@router.get("/missions/{farm_id}", response_model=list[DroneMissionRead])
def missions(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[DroneMission]:
    FarmService(db).get_for_user(farm_id, current_user)
    return DroneService(db).missions_for_farm(farm_id)


@router.post("/missions", response_model=DroneMissionRead, status_code=status.HTTP_201_CREATED)
def create_mission(
    payload: DroneMissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DroneMission:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return DroneService(db).create_mission(payload, current_user)
