from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: RegisterRequest) -> TokenResponse:
        existing = self.db.scalar(select(User).where(User.email == payload.email.lower()))
        if existing:
            raise ConflictError("An account with this email already exists.")

        user = User(
            full_name=payload.full_name,
            email=payload.email.lower(),
            phone=payload.phone,
            password_hash=hash_password(payload.password),
            role=payload.role,
            preferred_language=payload.preferred_language,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return self._token_for_user(user)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.db.scalar(select(User).where(User.email == email.lower()))
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password.")
        if not user.is_active:
            raise UnauthorizedError("This account is disabled.")
        return self._token_for_user(user)

    def _token_for_user(self, user: User) -> TokenResponse:
        token = create_access_token(str(user.id), {"role": user.role.value})
        return TokenResponse(access_token=token, user=user)
