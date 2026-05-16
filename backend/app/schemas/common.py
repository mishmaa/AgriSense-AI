import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


class IdResponse(BaseModel):
    id: uuid.UUID


class TimestampedSchema(ORMModel):
    created_at: datetime
    updated_at: datetime
