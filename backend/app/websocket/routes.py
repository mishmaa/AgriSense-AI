import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from app.core.security import decode_access_token
from app.websocket.manager import connection_manager


router = APIRouter(tags=["WebSockets"])


def _validate_ws_token(token: str | None) -> uuid.UUID | None:
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        return uuid.UUID(str(payload.get("sub")))
    except (TypeError, ValueError):
        return None


@router.websocket("/ws/sensors/{farm_id}")
async def sensor_stream(websocket: WebSocket, farm_id: uuid.UUID, token: str | None = None) -> None:
    user_id = _validate_ws_token(token)
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await connection_manager.connect_sensor_stream(farm_id, websocket)
    try:
        await websocket.send_json(
            {
                "type": "connected",
                "stream": "sensors",
                "farm_id": str(farm_id),
                "connected_at": datetime.now(UTC).isoformat(),
            }
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect_sensor_stream(farm_id, websocket)


@router.websocket("/ws/alerts/{user_id}")
async def alert_stream(websocket: WebSocket, user_id: uuid.UUID, token: str | None = None) -> None:
    token_user_id = _validate_ws_token(token)
    if token_user_id != user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await connection_manager.connect_alert_stream(user_id, websocket)
    try:
        await websocket.send_json(
            {
                "type": "connected",
                "stream": "alerts",
                "user_id": str(user_id),
                "connected_at": datetime.now(UTC).isoformat(),
            }
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect_alert_stream(user_id, websocket)
