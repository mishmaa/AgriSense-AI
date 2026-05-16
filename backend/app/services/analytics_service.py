from uuid import UUID

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.irrigation import IrrigationEvent
from app.models.notification import Notification
from app.models.sensor import Sensor, SensorReading
from app.services.cache_service import app_cache
from app.schemas.analytics import DashboardAnalytics, MetricCard


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def dashboard(self, farm_id: UUID) -> DashboardAnalytics:
        cache_key = f"analytics:{farm_id}:dashboard"
        cached = app_cache.get(cache_key)
        if cached:
            return cached

        active_sensors = self.db.scalar(select(func.count(Sensor.id)).where(Sensor.farm_id == farm_id)) or 0
        unread_alerts = (
            self.db.scalar(
                select(func.count(Notification.id)).where(
                    Notification.farm_id == farm_id,
                    Notification.is_read.is_(False),
                )
            )
            or 0
        )
        latest = self.db.scalar(
            select(SensorReading)
            .where(SensorReading.farm_id == farm_id)
            .order_by(desc(SensorReading.recorded_at))
            .limit(1)
        )
        irrigation_count = (
            self.db.scalar(select(func.count(IrrigationEvent.id)).where(IrrigationEvent.farm_id == farm_id)) or 0
        )

        metrics = []
        if latest:
            metrics = [
                MetricCard(label="Soil moisture", value=latest.soil_moisture or 0, unit="%"),
                MetricCard(label="Temperature", value=latest.temperature or 0, unit="C"),
                MetricCard(label="Humidity", value=latest.humidity or 0, unit="%"),
                MetricCard(label="Tank level", value=latest.water_tank_level or 0, unit="%"),
                MetricCard(label="Wind speed", value=latest.wind_speed or 0, unit="km/h"),
            ]

        return app_cache.set(
            cache_key,
            DashboardAnalytics(
                health_score=88.5 if active_sensors else 0,
                active_sensors=active_sensors,
                unread_alerts=unread_alerts,
                latest_metrics=metrics,
                irrigation_summary={"events": irrigation_count, "mode": "hybrid"},
                weather_risk="low",
            ),
            ttl_seconds=20,
        )
