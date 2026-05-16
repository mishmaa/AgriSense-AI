from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from simulator import PROFILE_PATH, SensorSimulator


def generate_history(sensor_id: str, profile: str, hours: int, interval_minutes: int, output: Path) -> None:
    profiles = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    simulator = SensorSimulator(profiles[profile])
    rows = []
    total = int((hours * 60) / interval_minutes)
    start = datetime.now(UTC) - timedelta(hours=hours)
    for index in range(total):
        reading = simulator.next_reading(sensor_id)
        reading["recorded_at"] = (start + timedelta(minutes=index * interval_minutes)).isoformat()
        rows.append(reading)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
      writer = csv.DictWriter(file, fieldnames=rows[0].keys())
      writer.writeheader()
      writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate historical AgriSense sensor data")
    parser.add_argument("--sensor-id", default="00000000-0000-0000-0000-000000000101")
    parser.add_argument("--profile", default="green_valley_multi_sensor")
    parser.add_argument("--hours", type=int, default=168)
    parser.add_argument("--interval-minutes", type=int, default=15)
    parser.add_argument("--output", type=Path, default=Path("history/sensor_history.csv"))
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_history(args.sensor_id, args.profile, args.hours, args.interval_minutes, args.output)
    print(args.output)
