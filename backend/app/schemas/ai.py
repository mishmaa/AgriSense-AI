import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import RecommendationType, Severity
from app.schemas.common import ORMModel


class CropRecommendationRequest(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    nitrogen: Decimal = Field(ge=0)
    phosphorus: Decimal = Field(ge=0)
    potassium: Decimal = Field(ge=0)
    temperature: Decimal
    humidity: Decimal = Field(ge=0, le=100)
    ph_level: Decimal = Field(ge=0, le=14)
    rainfall_mm: Decimal = Field(ge=0)
    soil_type: str


class FertilizerRecommendationRequest(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    crop_name: str
    growth_stage: str
    soil_type: str = "loam"
    nitrogen: Decimal = Field(ge=0)
    phosphorus: Decimal = Field(ge=0)
    potassium: Decimal = Field(ge=0)
    ph_level: Decimal = Field(ge=0, le=14)


class YieldPredictionRequest(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    crop_name: str
    farm_area_hectares: Decimal = Field(gt=0)
    rainfall_mm: Decimal = Field(ge=0)
    avg_temperature: Decimal
    irrigation_events_count: int = Field(ge=0)
    fertilizer_score: Decimal = Field(ge=0, le=1)
    avg_humidity: Decimal = Field(default=65, ge=0, le=100)
    soil_health_score: Decimal = Field(default=0.78, ge=0, le=1)


class IrrigationPredictionRequest(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    soil_moisture: Decimal = Field(ge=0, le=100)
    temperature: Decimal
    humidity: Decimal = Field(ge=0, le=100)
    rainfall_forecast_mm: Decimal = Field(default=0, ge=0)
    water_tank_level: Decimal = Field(ge=0, le=100)
    crop_stage: str = "vegetative"
    soil_type: str = "loam"
    hour_of_day: int = Field(default=8, ge=0, le=23)


class WeatherSuggestionRequest(BaseModel):
    farm_id: uuid.UUID
    crop_name: str
    condition: str
    temperature: Decimal
    humidity: Decimal = Field(ge=0, le=100)
    rainfall_mm: Decimal = Field(default=0, ge=0)
    wind_speed: Decimal = Field(default=0, ge=0)


class DiseaseFeatureDetectionRequest(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    crop_name: str
    image_url: str | None = None
    leaf_green_index: Decimal = Field(default=0.62, ge=0, le=1)
    spot_ratio: Decimal = Field(default=0.18, ge=0, le=1)
    yellowing_ratio: Decimal = Field(default=0.2, ge=0, le=1)
    texture_score: Decimal = Field(default=0.55, ge=0, le=1)
    edge_damage: Decimal = Field(default=0.12, ge=0, le=1)


class AIRecommendationRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None
    user_id: uuid.UUID
    recommendation_type: RecommendationType
    title: str
    result: dict[str, Any]
    input_features: dict[str, Any]
    confidence_score: Decimal
    model_version: str
    created_at: datetime


class AIPredictionResponse(BaseModel):
    prediction: str | float
    confidence_score: Decimal
    explanation: str
    model_version: str
    actions: list[str]
    metadata: dict[str, Any]


class DiseaseDetectionCreate(BaseModel):
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None = None
    crop_name: str
    image_url: str


class DiseaseDetectionRead(ORMModel):
    id: uuid.UUID
    farm_id: uuid.UUID
    zone_id: uuid.UUID | None
    user_id: uuid.UUID
    crop_name: str
    image_url: str
    disease_name: str
    severity: Severity
    confidence_score: Decimal
    treatment_advice: str
    prevention_advice: str
    created_at: datetime
