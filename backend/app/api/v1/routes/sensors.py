from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.iot.alert_engine import evaluate_sensor_alerts
from app.models.farm import Farm
from app.models.enums import NotificationChannel
from app.models.sensor import Sensor, SensorReading
from app.models.user import User
from app.schemas.notification import NotificationCreate
from app.schemas.sensor import SensorCreate, SensorRead, SensorReadingBatchCreate, SensorReadingCreate, SensorReadingRead
from app.services.farm_service import FarmService
from app.services.notification_service import NotificationService
from app.services.sensor_service import SensorService
from app.websocket.manager import connection_manager


router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorRead, status_code=status.HTTP_201_CREATED)
def create_sensor(
    payload: SensorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Sensor:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return SensorService(db).create_sensor(payload)


@router.get("/farm/{farm_id}", response_model=list[SensorRead])
def sensors_for_farm(
    farm_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Sensor]:
    FarmService(db).get_for_user(farm_id, current_user)
    return SensorService(db).list_by_farm(farm_id)


@router.post("/readings", response_model=SensorReadingRead, status_code=status.HTTP_201_CREATED)
async def ingest_reading(
    payload: SensorReadingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SensorReading:
    sensor = db.get(Sensor, payload.sensor_id)
    if sensor:
        FarmService(db).get_for_user(sensor.farm_id, current_user)
    reading = SensorService(db).ingest_reading(payload)
    await _broadcast_reading_and_alerts(reading, db)
    return reading


@router.post("/readings/batch", response_model=list[SensorReadingRead], status_code=status.HTTP_201_CREATED)
async def ingest_readings_batch(
    payload: SensorReadingBatchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SensorReading]:
    checked_farms: set[UUID] = set()
    for reading_payload in payload.readings:
        sensor = db.get(Sensor, reading_payload.sensor_id)
        if sensor and sensor.farm_id not in checked_farms:
            FarmService(db).get_for_user(sensor.farm_id, current_user)
            checked_farms.add(sensor.farm_id)
    readings = SensorService(db).ingest_readings_batch(payload.readings)
    for reading in readings[-25:]:
        await _broadcast_reading_and_alerts(reading, db)
    return readings


async def _broadcast_reading_and_alerts(reading: SensorReading, db: Session) -> None:
    await connection_manager.broadcast_sensor(
        reading.farm_id,
        {
            "type": "sensor_reading",
            "farm_id": str(reading.farm_id),
            "zone_id": str(reading.zone_id) if reading.zone_id else None,
            "reading": SensorReadingRead.model_validate(reading).model_dump(mode="json"),
        },
    )

    farm = db.get(Farm, reading.farm_id)
    if farm:
        notification_service = NotificationService(db)
        for alert in evaluate_sensor_alerts(reading):
            notification = notification_service.create(
                NotificationCreate(
                    user_id=farm.owner_id,
                    farm_id=reading.farm_id,
                    notification_type=alert.alert_type,
                    channel=NotificationChannel.IN_APP,
                    severity=alert.severity,
                    title=alert.title,
                    message=alert.message,
                    metadata=alert.metadata or {},
                )
            )
            await connection_manager.broadcast_alert(
                farm.owner_id,
                {
                    "type": "sensor_alert",
                    "notification_id": str(notification.id),
                    "farm_id": str(reading.farm_id),
                    "severity": notification.severity.value,
                    "title": notification.title,
                    "message": notification.message,
                    "metadata": notification.metadata_json,
                },
            )
            if alert.severity.value == "critical":
                owner = db.get(User, farm.owner_id)
                notification_service.create(
                    NotificationCreate(
                        user_id=farm.owner_id,
                        farm_id=reading.farm_id,
                        notification_type=alert.alert_type,
                        channel=NotificationChannel.SMS,
                        severity=alert.severity,
                        title=alert.title,
                        message=alert.message,
                        metadata=alert.metadata or {},
                    )
                )
                notification_service.create(
                    NotificationCreate(
                        user_id=farm.owner_id,
                        farm_id=reading.farm_id,
                        notification_type=alert.alert_type,
                        channel=NotificationChannel.EMAIL,
                        severity=alert.severity,
                        title=alert.title,
                        message=f"{alert.message}\n\nFarm owner: {owner.full_name if owner else 'Unknown'}",
                        metadata=alert.metadata or {},
                    )
                )


@router.get("/readings/{farm_id}", response_model=list[SensorReadingRead])
def readings_for_farm(
    farm_id: UUID,
    limit: int = Query(default=200, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SensorReading]:
    FarmService(db).get_for_user(farm_id, current_user)
    return SensorService(db).readings_for_farm(farm_id, limit)
