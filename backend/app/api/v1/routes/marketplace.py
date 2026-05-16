from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.marketplace import MarketplaceItem
from app.models.user import User
from app.schemas.marketplace import MarketplaceItemCreate, MarketplaceItemRead, MarketplaceItemUpdate
from app.services.marketplace_service import MarketplaceService


router = APIRouter(prefix="/marketplace", tags=["Marketplace"])


@router.get("/", response_model=list[MarketplaceItemRead])
def list_marketplace(db: Session = Depends(get_db)) -> list[MarketplaceItem]:
    return MarketplaceService(db).list_active()


@router.post("/", response_model=MarketplaceItemRead, status_code=status.HTTP_201_CREATED)
def create_marketplace_item(
    payload: MarketplaceItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MarketplaceItem:
    return MarketplaceService(db).create(payload, current_user)


@router.patch("/{item_id}", response_model=MarketplaceItemRead)
def update_marketplace_item(
    item_id: UUID,
    payload: MarketplaceItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MarketplaceItem:
    return MarketplaceService(db).update(item_id, payload, current_user)
