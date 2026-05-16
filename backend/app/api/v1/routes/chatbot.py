from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.chatbot import ChatbotMessageRead, ChatbotRequest, ChatbotResponse
from app.services.chatbot_service import ChatbotService
from app.services.farm_service import FarmService


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/message", response_model=ChatbotResponse)
def send_message(
    payload: ChatbotRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ChatbotResponse:
    if payload.farm_id:
        FarmService(db).get_for_user(payload.farm_id, current_user)
    messages = ChatbotService(db).send_message(payload, current_user)
    return ChatbotResponse(reply=messages[-1].message, conversation=messages)


@router.get("/history", response_model=list[ChatbotMessageRead])
def history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ChatbotService(db).history(current_user)
