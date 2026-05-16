import uuid
from collections import defaultdict
from typing import Any

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.sensor_connections: dict[uuid.UUID, list[WebSocket]] = defaultdict(list)
        self.alert_connections: dict[uuid.UUID, list[WebSocket]] = defaultdict(list)

    async def connect_sensor_stream(self, farm_id: uuid.UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.sensor_connections[farm_id].append(websocket)

    async def connect_alert_stream(self, user_id: uuid.UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self.alert_connections[user_id].append(websocket)

    def disconnect_sensor_stream(self, farm_id: uuid.UUID, websocket: WebSocket) -> None:
        self._disconnect(self.sensor_connections[farm_id], websocket)

    def disconnect_alert_stream(self, user_id: uuid.UUID, websocket: WebSocket) -> None:
        self._disconnect(self.alert_connections[user_id], websocket)

    async def broadcast_sensor(self, farm_id: uuid.UUID, payload: dict[str, Any]) -> None:
        await self._broadcast(self.sensor_connections[farm_id], payload)

    async def broadcast_alert(self, user_id: uuid.UUID, payload: dict[str, Any]) -> None:
        await self._broadcast(self.alert_connections[user_id], payload)

    def _disconnect(self, connections: list[WebSocket], websocket: WebSocket) -> None:
        if websocket in connections:
            connections.remove(websocket)

    async def _broadcast(self, connections: list[WebSocket], payload: dict[str, Any]) -> None:
        stale: list[WebSocket] = []
        for websocket in connections:
            try:
                await websocket.send_json(payload)
            except RuntimeError:
                stale.append(websocket)
        for websocket in stale:
            self._disconnect(connections, websocket)


connection_manager = ConnectionManager()
