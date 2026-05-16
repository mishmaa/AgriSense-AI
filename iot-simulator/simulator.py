from __future__ import annotations

import argparse
import asyncio
import json
import math
import random
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx


PROFILE_PATH = Path(__file__).with_name("sensor_profiles.json")


@dataclass
class FarmState:
    soil_moisture: float
    temperature: float
    humidity: float
    ph_level: float
    water_tank_level: float
    light_intensity: float
    wind_speed: float
    rain_mm: float = 0


class SensorSimulator:
    def __init__(self, profile: dict[str, Any]):
        self.profile = profile
        self.state = FarmState(
            soil_moisture=float(profile["base_soil_moisture"]),
            temperature=float(profile["base_temperature"]),
            humidity=float(profile["base_humidity"]),
            ph_level=float(profile["base_ph"]),
            water_tank_level=float(profile["base_tank"]),
            light_intensity=float(profile["base_light"]),
            wind_speed=float(profile["base_wind"]),
        )
        self.tick = 0

    def next_reading(self, sensor_id: str) -> dict[str, Any]:
        self.tick += 1
        hour = datetime.now().hour
        daylight = max(0, math.sin((hour - 6) / 12 * math.pi))
        heat_curve = math.sin((hour - 7) / 12 * math.pi)
        heat_curve = max(-0.35, heat_curve)

        rain_event = random.random() < 0.06
        self.state.rain_mm = round(random.uniform(1.5, 18), 2) if rain_event else max(0, self.state.rain_mm * 0.45)
        irrigation_pulse = self.state.soil_moisture < 31 and self.state.water_tank_level > 20

        self.state.temperature = _clamp(self.profile["base_temperature"] + heat_curve * 7 + random.gauss(0, 0.7), 12, 42)
        self.state.humidity = _clamp(self.profile["base_humidity"] - heat_curve * 12 + self.state.rain_mm * 0.6 + random.gauss(0, 2.2), 25, 98)
        moisture_delta = -0.18 - daylight * 0.35 + self.state.rain_mm * 0.18 + (7.5 if irrigation_pulse else 0)
        self.state.soil_moisture = _clamp(self.state.soil_moisture + moisture_delta + random.gauss(0, 0.55), 12, 92)
        tank_delta = -0.05 - (3.4 if irrigation_pulse else 0) + (0.6 if rain_event else 0)
        self.state.water_tank_level = _clamp(self.state.water_tank_level + tank_delta + random.gauss(0, 0.18), 3, 100)
        self.state.ph_level = _clamp(self.state.ph_level + random.gauss(0, 0.015), 4.8, 8.4)
        self.state.light_intensity = _clamp(daylight * self.profile["base_light"] + random.gauss(0, 1800), 0, 92000)
        self.state.wind_speed = _clamp(self.profile["base_wind"] + random.gauss(0, 3.5) + (random.uniform(10, 22) if random.random() < 0.04 else 0), 0, 58)

        anomaly = 0.0
        if self.state.soil_moisture < 30 or self.state.temperature > 36 or self.state.water_tank_level < 20:
            anomaly = round(random.uniform(0.7, 0.96), 3)

        return {
            "sensor_id": sensor_id,
            "soil_moisture": round(self.state.soil_moisture, 2),
            "temperature": round(self.state.temperature, 2),
            "humidity": round(self.state.humidity, 2),
            "water_tank_level": round(self.state.water_tank_level, 2),
            "ph_level": round(self.state.ph_level, 2),
            "rainfall_mm": round(self.state.rain_mm, 2),
            "light_intensity": round(self.state.light_intensity, 2),
            "wind_speed": round(self.state.wind_speed, 2),
            "anomaly_score": anomaly,
            "recorded_at": datetime.now(UTC).isoformat()
        }


async def run(args: argparse.Namespace) -> None:
    profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    simulator = SensorSimulator(profiles[args.profile])
    headers = {"Authorization": f"Bearer {args.token}"} if args.token else {}

    async with httpx.AsyncClient(timeout=10, trust_env=False) as client:
        for _ in range(args.count):
            reading = simulator.next_reading(args.sensor_id)
            if args.dry_run:
                print(json.dumps(reading, indent=2))
            else:
                response = await client.post(f"{args.api_url.rstrip('/')}/sensors/readings", json=reading, headers=headers)
                response.raise_for_status()
                print(f"posted {reading['recorded_at']} moisture={reading['soil_moisture']} tank={reading['water_tank_level']}")
            await asyncio.sleep(args.interval)


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AgriSense AI realtime IoT simulator")
    parser.add_argument("--api-url", default="http://localhost:8000/api/v1")
    parser.add_argument("--token", default="")
    parser.add_argument("--sensor-id", default="00000000-0000-0000-0000-000000000101")
    parser.add_argument("--profile", default="green_valley_multi_sensor")
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--count", type=int, default=120)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))
