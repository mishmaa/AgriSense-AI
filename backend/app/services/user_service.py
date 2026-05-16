from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.created_at.desc())))

    def get_user(self, user_id: UUID) -> User:
        user = self.db.get(User, user_id)
        if not user:
            raise NotFoundError("User not found.")
        return user

    def update_user(self, user: User, payload: UserUpdate) -> User:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
