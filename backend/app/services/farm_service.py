from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.farm import Farm, FarmZone
from app.models.user import User
from app.schemas.farm import FarmCreate, FarmUpdate


class FarmService:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user: User) -> list[Farm]:
        query = select(Farm).options(selectinload(Farm.zones)).order_by(Farm.created_at.desc())
        if user.role.value != "admin":
            query = query.where(Farm.owner_id == user.id)
        return list(self.db.scalars(query))

    def create(self, owner: User, payload: FarmCreate) -> Farm:
        zones_payload = payload.zones
        farm_data = payload.model_dump(exclude={"zones"})
        farm = Farm(owner_id=owner.id, **farm_data)
        farm.zones = [FarmZone(**zone.model_dump()) for zone in zones_payload]
        self.db.add(farm)
        self.db.commit()
        self.db.refresh(farm)
        return self.get_for_user(farm.id, owner)

    def get_for_user(self, farm_id: UUID, user: User) -> Farm:
        farm = self.db.scalar(
            select(Farm).options(selectinload(Farm.zones)).where(Farm.id == farm_id)
        )
        if not farm:
            raise NotFoundError("Farm not found.")
        if user.role.value != "admin" and farm.owner_id != user.id:
            raise ForbiddenError("You do not have access to this farm.")
        return farm

    def update(self, farm_id: UUID, user: User, payload: FarmUpdate) -> Farm:
        farm = self.get_for_user(farm_id, user)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(farm, key, value)
        self.db.commit()
        self.db.refresh(farm)
        return farm

    def delete(self, farm_id: UUID, user: User) -> None:
        farm = self.get_for_user(farm_id, user)
        self.db.delete(farm)
        self.db.commit()
