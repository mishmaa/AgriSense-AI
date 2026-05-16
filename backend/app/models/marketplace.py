import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.enums import MarketplaceCategory, MarketplaceStatus


class MarketplaceItem(TimestampMixin, Base):
    __tablename__ = "marketplace_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    seller_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    category: Mapped[MarketplaceCategory] = mapped_column(Enum(MarketplaceCategory), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    unit: Mapped[str] = mapped_column(String(40))
    image_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[MarketplaceStatus] = mapped_column(Enum(MarketplaceStatus), default=MarketplaceStatus.ACTIVE)

    seller: Mapped["User"] = relationship(back_populates="marketplace_items")
