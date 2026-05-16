from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.enums import MarketplaceStatus
from app.models.marketplace import MarketplaceItem
from app.models.user import User
from app.schemas.marketplace import MarketplaceItemCreate, MarketplaceItemUpdate


class MarketplaceService:
    def __init__(self, db: Session):
        self.db = db

    def list_active(self) -> list[MarketplaceItem]:
        query = (
            select(MarketplaceItem)
            .where(MarketplaceItem.status == MarketplaceStatus.ACTIVE)
            .order_by(desc(MarketplaceItem.created_at))
        )
        return list(self.db.scalars(query))

    def create(self, payload: MarketplaceItemCreate, seller: User) -> MarketplaceItem:
        item = MarketplaceItem(seller_id=seller.id, **payload.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item_id: UUID, payload: MarketplaceItemUpdate, user: User) -> MarketplaceItem:
        item = self.db.get(MarketplaceItem, item_id)
        if not item:
            raise NotFoundError("Marketplace item not found.")
        if item.seller_id != user.id and user.role.value != "admin":
            raise ForbiddenError("You can only update your own listings.")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item
