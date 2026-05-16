from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.ai.engine import ai_engine
from app.models.chatbot import ChatbotMessage
from app.models.enums import ChatRole
from app.models.user import User
from app.schemas.chatbot import ChatbotRequest


class ChatbotService:
    def __init__(self, db: Session):
        self.db = db

    def send_message(self, payload: ChatbotRequest, user: User) -> list[ChatbotMessage]:
        user_message = ChatbotMessage(
            user_id=user.id,
            farm_id=payload.farm_id,
            role=ChatRole.USER,
            message=payload.message,
            language=payload.language,
            metadata_json={},
        )
        prediction = ai_engine.chatbot_reply(payload.message, {"farm_id": str(payload.farm_id) if payload.farm_id else None})
        assistant_message = ChatbotMessage(
            user_id=user.id,
            farm_id=payload.farm_id,
            role=ChatRole.ASSISTANT,
            message=str(prediction.prediction),
            language=payload.language,
            metadata_json={
                "engine": prediction.model_version,
                "confidence": prediction.confidence,
                "explanation": prediction.explanation,
                "actions": prediction.actions,
                **prediction.metadata,
            },
        )
        self.db.add_all([user_message, assistant_message])
        self.db.commit()
        self.db.refresh(user_message)
        self.db.refresh(assistant_message)
        return [user_message, assistant_message]

    def history(self, user: User, limit: int = 50) -> list[ChatbotMessage]:
        query = (
            select(ChatbotMessage)
            .where(ChatbotMessage.user_id == user.id)
            .order_by(desc(ChatbotMessage.created_at))
            .limit(limit)
        )
        return list(reversed(list(self.db.scalars(query))))
