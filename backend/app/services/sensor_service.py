from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.sensor import Sensor, SensorReading
from app.services.cache_service import app_cache
from app.schemas.sensor import SensorCreate, SensorReadingCreate


class SensorService:
    def __init__(self, db: Session):
        self.db = db

    def create_sensor(self, payload: SensorCreate) -> Sensor:
        sensor = Sensor(**payload.model_dump(), last_seen_at=datetime.now(UTC))
        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def list_by_farm(self, farm_id: UUID) -> list[Sensor]:
        return list(self.db.scalars(select(Sensor).where(Sensor.farm_id == farm_id)))

    def ingest_reading(self, payload: SensorReadingCreate) -> SensorReading:
        reading = self._build_reading(payload)
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)
        app_cache.invalidate_prefix(f"analytics:{reading.farm_id}")
        return reading

    def ingest_readings_batch(self, payloads: list[SensorReadingCreate]) -> list[SensorReading]:
        readings = [self._build_reading(payload) for payload in payloads]
        self.db.add_all(readings)
        self.db.commit()
        farm_ids = set()
        for reading in readings:
            self.db.refresh(reading)
            farm_ids.add(reading.farm_id)
        for farm_id in farm_ids:
            app_cache.invalidate_prefix(f"analytics:{farm_id}")
        return readings

    def _build_reading(self, payload: SensorReadingCreate) -> SensorReading:
        sensor = self.db.get(Sensor, payload.sensor_id)
        if not sensor:
            raise NotFoundError("Sensor not found.")
        data = payload.model_dump()
        data["recorded_at"] = data["recorded_at"] or datetime.now(UTC)
        sensor.last_seen_at = datetime.now(UTC)
        return SensorReading(**data, farm_id=sensor.farm_id, zone_id=sensor.zone_id)

    def readings_for_farm(self, farm_id: UUID, limit: int = 200) -> list[SensorReading]:
        query = (
            select(SensorReading)
            .where(SensorReading.farm_id == farm_id)
            .order_by(desc(SensorReading.recorded_at))
            .limit(limit)
        )
        return list(self.db.scalars(query))
