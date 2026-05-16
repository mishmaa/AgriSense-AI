from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.farm import Farm
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.farm import FarmCreate, FarmRead, FarmUpdate
from app.services.farm_service import FarmService


router = APIRouter(prefix="/farms", tags=["Farms"])


@router.get("/", response_model=list[FarmRead])
def list_farms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Farm]:
    return FarmService(db).list_for_user(current_user)


@router.post("/", response_model=FarmRead, status_code=status.HTTP_201_CREATED)
def create_farm(
    payload: FarmCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Farm:
    return FarmService(db).create(current_user, payload)


@router.get("/{farm_id}", response_model=FarmRead)
def get_farm(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Farm:
    return FarmService(db).get_for_user(farm_id, current_user)


@router.patch("/{farm_id}", response_model=FarmRead)
def update_farm(
    farm_id: UUID,
    payload: FarmUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Farm:
    return FarmService(db).update(farm_id, current_user, payload)


@router.delete("/{farm_id}", response_model=MessageResponse)
def delete_farm(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    FarmService(db).delete(farm_id, current_user)
    return MessageResponse(message="Farm deleted.")
