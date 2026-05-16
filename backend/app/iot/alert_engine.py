from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from app.models.enums import NotificationSeverity, NotificationType
from app.models.sensor import SensorReading


@dataclass
class SensorAlert:
    title: str
    message: str
    severity: NotificationSeverity
    alert_type: NotificationType = NotificationType.SENSOR
    metadata: dict[str, Any] | None = None


def evaluate_sensor_alerts(reading: SensorReading) -> list[SensorAlert]:
    alerts: list[SensorAlert] = []

    soil_moisture = _float(reading.soil_moisture)
    temperature = _float(reading.temperature)
    humidity = _float(reading.humidity)
    tank = _float(reading.water_tank_level)
    ph = _float(reading.ph_level)
    rainfall = _float(reading.rainfall_mm)
    wind = _float(reading.wind_speed)

    if soil_moisture is not None and soil_moisture < 30:
        alerts.append(
            SensorAlert(
                title="Critical soil moisture",
                message=f"Soil moisture dropped to {soil_moisture:.1f}%. Start irrigation or inspect the zone.",
                severity=NotificationSeverity.CRITICAL,
                metadata={"metric": "soil_moisture", "value": soil_moisture},
            )
        )
    if temperature is not None and temperature > 36:
        alerts.append(
            SensorAlert(
                title="Heat stress warning",
                message=f"Temperature reached {temperature:.1f} C. Protect sensitive crops and irrigate early.",
                severity=NotificationSeverity.WARNING,
                metadata={"metric": "temperature", "value": temperature},
            )
        )
    if humidity is not None and rainfall is not None and humidity > 88 and rainfall > 2:
        alerts.append(
            SensorAlert(
                title="Fungal disease risk",
                message="High humidity with rainfall increases fungal disease pressure. Increase leaf scouting.",
                severity=NotificationSeverity.WARNING,
                metadata={"metric": "humidity_rainfall", "humidity": humidity, "rainfall_mm": rainfall},
            )
        )
    if tank is not None and tank < 20:
        alerts.append(
            SensorAlert(
                title="Low water tank",
                message=f"Tank level is {tank:.1f}%. Refill before automatic irrigation continues.",
                severity=NotificationSeverity.CRITICAL,
                metadata={"metric": "water_tank_level", "value": tank},
            )
        )
    if ph is not None and (ph < 5.5 or ph > 8.0):
        alerts.append(
            SensorAlert(
                title="Soil pH out of range",
                message=f"Soil pH is {ph:.2f}. Schedule a soil chemistry check.",
                severity=NotificationSeverity.WARNING,
                metadata={"metric": "ph_level", "value": ph},
            )
        )
    if wind is not None and wind > 35:
        alerts.append(
            SensorAlert(
                title="High wind warning",
                message=f"Wind speed reached {wind:.1f} km/h. Delay spraying and drone operations.",
                severity=NotificationSeverity.WARNING,
                metadata={"metric": "wind_speed", "value": wind},
            )
        )

    return alerts


def _float(value: Decimal | None) -> float | None:
    return float(value) if value is not None else None
