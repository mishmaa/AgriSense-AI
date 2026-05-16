from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.ai import AIRecommendation, DiseaseDetection
from app.models.user import User
from app.schemas.ai import (
    AIRecommendationRead,
    CropRecommendationRequest,
    DiseaseDetectionCreate,
    DiseaseFeatureDetectionRequest,
    DiseaseDetectionRead,
    FertilizerRecommendationRequest,
    IrrigationPredictionRequest,
    WeatherSuggestionRequest,
    YieldPredictionRequest,
)
from app.services.ai_service import AIService
from app.services.farm_service import FarmService


router = APIRouter(prefix="/ai", tags=["AI Recommendations"])
disease_router = APIRouter(prefix="/disease-detection", tags=["Disease Detection"])


@router.post("/crop-recommendation", response_model=AIRecommendationRead)
def crop_recommendation(
    payload: CropRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIRecommendation:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).crop_recommendation(payload, current_user)


@router.post("/fertilizer-recommendation", response_model=AIRecommendationRead)
def fertilizer_recommendation(
    payload: FertilizerRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIRecommendation:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).fertilizer_recommendation(payload, current_user)


@router.post("/yield-prediction", response_model=AIRecommendationRead)
def yield_prediction(
    payload: YieldPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIRecommendation:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).yield_prediction(payload, current_user)


@router.post("/irrigation-prediction", response_model=AIRecommendationRead)
def irrigation_prediction(
    payload: IrrigationPredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIRecommendation:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).irrigation_prediction(payload, current_user)


@router.post("/weather-suggestion", response_model=AIRecommendationRead)
def weather_suggestion(
    payload: WeatherSuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIRecommendation:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).weather_suggestion(payload, current_user)


@disease_router.post("/", response_model=DiseaseDetectionRead)
def detect_disease(
    payload: DiseaseDetectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DiseaseDetection:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).detect_disease(payload, current_user)


@disease_router.post("/features", response_model=DiseaseDetectionRead)
def detect_disease_from_features(
    payload: DiseaseFeatureDetectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DiseaseDetection:
    FarmService(db).get_for_user(payload.farm_id, current_user)
    return AIService(db).detect_disease_from_features(payload, current_user)
