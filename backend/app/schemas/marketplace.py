import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import MarketplaceCategory, MarketplaceStatus
from app.schemas.common import ORMModel


class MarketplaceItemCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    category: MarketplaceCategory
    description: str
    price: Decimal = Field(ge=0)
    quantity: Decimal = Field(gt=0)
    unit: str = Field(min_length=1, max_length=40)
    image_url: str | None = Field(default=None, max_length=500)


class MarketplaceItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0)
    quantity: Decimal | None = Field(default=None, gt=0)
    status: MarketplaceStatus | None = None


class MarketplaceItemRead(ORMModel):
    id: uuid.UUID
    seller_id: uuid.UUID
    title: str
    category: MarketplaceCategory
    description: str
    price: Decimal
    quantity: Decimal
    unit: str
    image_url: str | None
    status: MarketplaceStatus
    created_at: datetime
