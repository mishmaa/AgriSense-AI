from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.weather import WeatherSnapshot
from app.schemas.weather import WeatherSnapshotCreate


class WeatherService:
    def __init__(self, db: Session):
        self.db = db

    def create_snapshot(self, payload: WeatherSnapshotCreate) -> WeatherSnapshot:
        data = payload.model_dump()
        data["captured_at"] = data["captured_at"] or datetime.now(UTC)
        snapshot = WeatherSnapshot(**data)
        self.db.add(snapshot)
        self.db.commit()
        self.db.refresh(snapshot)
        return snapshot

    def latest_for_farm(self, farm_id: UUID, limit: int = 24) -> list[WeatherSnapshot]:
        query = (
            select(WeatherSnapshot)
            .where(WeatherSnapshot.farm_id == farm_id)
            .order_by(desc(WeatherSnapshot.captured_at))
            .limit(limit)
        )
        return list(self.db.scalars(query))
