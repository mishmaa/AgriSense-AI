from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.drone import DroneMission
from app.models.user import User
from app.schemas.drone import DroneMissionCreate


class DroneService:
    def __init__(self, db: Session):
        self.db = db

    def create_mission(self, payload: DroneMissionCreate, user: User) -> DroneMission:
        mission = DroneMission(created_by_id=user.id, **payload.model_dump())
        self.db.add(mission)
        self.db.commit()
        self.db.refresh(mission)
        return mission

    def missions_for_farm(self, farm_id: UUID) -> list[DroneMission]:
        query = (
            select(DroneMission)
            .where(DroneMission.farm_id == farm_id)
            .order_by(desc(DroneMission.scheduled_at))
        )
        return list(self.db.scalars(query))
