import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin
from app.db.types import JSONType
from app.models.enums import RecommendationType, Severity


class AIRecommendation(TimestampMixin, Base):
    __tablename__ = "ai_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farm_zones.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    recommendation_type: Mapped[RecommendationType] = mapped_column(Enum(RecommendationType), index=True)
    title: Mapped[str] = mapped_column(String(180))
    result: Mapped[dict] = mapped_column(JSONType)
    input_features: Mapped[dict] = mapped_column(JSONType)
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(5, 4))
    model_version: Mapped[str] = mapped_column(String(80), default="rules-v1")


class DiseaseDetection(TimestampMixin, Base):
    __tablename__ = "disease_detections"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("farms.id", ondelete="CASCADE"), index=True)
    zone_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("farm_zones.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    crop_name: Mapped[str] = mapped_column(String(120))
    image_url: Mapped[str] = mapped_column(String(500))
    disease_name: Mapped[str] = mapped_column(String(160))
    severity: Mapped[Severity] = mapped_column(Enum(Severity), default=Severity.LOW)
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(5, 4))
    treatment_advice: Mapped[str] = mapped_column(String(1000))
    prevention_advice: Mapped[str] = mapped_column(String(1000))
