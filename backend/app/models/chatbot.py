import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.db.types import JSONType
from app.models.enums import ChatRole


class ChatbotMessage(TimestampMixin, Base):
    __tablename__ = "chatbot_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    farm_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farms.id", ondelete="SET NULL"), index=True)
    role: Mapped[ChatRole] = mapped_column(Enum(ChatRole), index=True)
    message: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(12), default="en")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONType, default=dict)

    user: Mapped["User"] = relationship(back_populates="chatbot_messages")
