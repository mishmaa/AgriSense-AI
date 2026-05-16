from decimal import Decimal

from pydantic import BaseModel


class MetricCard(BaseModel):
    label: str
    value: Decimal | int | float | str
    unit: str | None = None
    trend: float | None = None


class DashboardAnalytics(BaseModel):
    health_score: float
    active_sensors: int
    unread_alerts: int
    latest_metrics: list[MetricCard]
    irrigation_summary: dict
    weather_risk: str
