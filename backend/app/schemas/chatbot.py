import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import ChatRole
from app.schemas.common import ORMModel


class ChatbotRequest(BaseModel):
    farm_id: uuid.UUID | None = None
    message: str = Field(min_length=1, max_length=3000)
    language: str = Field(default="en", max_length=12)


class ChatbotMessageRead(ORMModel):
    id: uuid.UUID
    user_id: uuid.UUID
    farm_id: uuid.UUID | None
    role: ChatRole
    message: str
    language: str
    metadata_json: dict[str, Any]
    created_at: datetime


class ChatbotResponse(BaseModel):
    reply: str
    conversation: list[ChatbotMessageRead]
