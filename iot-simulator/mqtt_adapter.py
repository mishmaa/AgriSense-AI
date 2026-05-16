from __future__ import annotations

import json
from typing import Any


class MQTTPublisher:
    """Optional MQTT publisher. Install paho-mqtt before using this adapter."""

    def __init__(self, host: str = "localhost", port: int = 1883, topic: str = "agrisense/sensors/readings"):
        try:
            import paho.mqtt.client as mqtt
        except ImportError as exc:
            raise RuntimeError("Install paho-mqtt to use MQTT integration: pip install paho-mqtt") from exc

        self.topic = topic
        self.client = mqtt.Client()
        self.client.connect(host, port, keepalive=60)

    def publish_reading(self, reading: dict[str, Any]) -> None:
        self.client.publish(self.topic, json.dumps(reading), qos=1)
