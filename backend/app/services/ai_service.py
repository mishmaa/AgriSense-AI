from decimal import Decimal

from sqlalchemy.orm import Session

from app.ai.engine import ai_engine
from app.models.ai import AIRecommendation, DiseaseDetection
from app.models.enums import RecommendationType, Severity
from app.models.user import User
from app.schemas.ai import (
    CropRecommendationRequest,
    DiseaseDetectionCreate,
    DiseaseFeatureDetectionRequest,
    FertilizerRecommendationRequest,
    IrrigationPredictionRequest,
    WeatherSuggestionRequest,
    YieldPredictionRequest,
)


class AIService:
    def __init__(self, db: Session):
        self.db = db

    def crop_recommendation(self, payload: CropRecommendationRequest, user: User) -> AIRecommendation:
        prediction = ai_engine.recommend_crop(payload.model_dump(mode="json"))
        result = self._result_payload("recommended_crop", prediction)
        return self._save_recommendation(
            payload.farm_id,
            payload.zone_id,
            user,
            RecommendationType.CROP,
            "AI crop recommendation",
            result,
            payload.model_dump(mode="json"),
            Decimal(str(prediction.confidence)),
        )

    def fertilizer_recommendation(
        self,
        payload: FertilizerRecommendationRequest,
        user: User,
    ) -> AIRecommendation:
        prediction = ai_engine.recommend_fertilizer(payload.model_dump(mode="json"))
        result = self._result_payload("fertilizer_plan", prediction)
        return self._save_recommendation(
            payload.farm_id,
            payload.zone_id,
            user,
            RecommendationType.FERTILIZER,
            "Fertilizer recommendation",
            result,
            payload.model_dump(mode="json"),
            Decimal(str(prediction.confidence)),
        )

    def yield_prediction(self, payload: YieldPredictionRequest, user: User) -> AIRecommendation:
        features = payload.model_dump(mode="json")
        features["area_hectares"] = features.pop("farm_area_hectares")
        features["irrigation_events"] = features.pop("irrigation_events_count")
        prediction = ai_engine.predict_yield(features)
        result = self._result_payload("predicted_yield_tons", prediction)
        return self._save_recommendation(
            payload.farm_id,
            payload.zone_id,
            user,
            RecommendationType.YIELD,
            "Yield prediction",
            result,
            payload.model_dump(mode="json"),
            Decimal(str(prediction.confidence)),
        )

    def irrigation_prediction(self, payload: IrrigationPredictionRequest, user: User) -> AIRecommendation:
        prediction = ai_engine.predict_irrigation(payload.model_dump(mode="json"))
        result = self._result_payload("irrigation_action", prediction)
        return self._save_recommendation(
            payload.farm_id,
            payload.zone_id,
            user,
            RecommendationType.IRRIGATION,
            "Irrigation prediction",
            result,
            payload.model_dump(mode="json"),
            Decimal(str(prediction.confidence)),
        )

    def weather_suggestion(self, payload: WeatherSuggestionRequest, user: User) -> AIRecommendation:
        prediction = ai_engine.suggest_weather_actions(payload.model_dump(mode="json"))
        result = self._result_payload("suggestion_type", prediction)
        return self._save_recommendation(
            payload.farm_id,
            None,
            user,
            RecommendationType.WEATHER_RISK,
            "Weather farming suggestion",
            result,
            payload.model_dump(mode="json"),
            Decimal(str(prediction.confidence)),
        )

    def detect_disease(self, payload: DiseaseDetectionCreate, user: User) -> DiseaseDetection:
        return self.detect_disease_from_features(
            DiseaseFeatureDetectionRequest(
                farm_id=payload.farm_id,
                zone_id=payload.zone_id,
                crop_name=payload.crop_name.lower(),
                image_url=payload.image_url,
            ),
            user,
        )

    def detect_disease_from_features(self, payload: DiseaseFeatureDetectionRequest, user: User) -> DiseaseDetection:
        prediction = ai_engine.detect_disease(payload.model_dump(mode="json"))
        severity = Severity.LOW
        if prediction.prediction != "healthy" and prediction.confidence >= 0.78:
            severity = Severity.MEDIUM
        if prediction.prediction != "healthy" and prediction.confidence >= 0.9:
            severity = Severity.HIGH
        detection = DiseaseDetection(
            farm_id=payload.farm_id,
            zone_id=payload.zone_id,
            user_id=user.id,
            crop_name=payload.crop_name,
            image_url=payload.image_url or "demo://leaf-feature-analysis",
            disease_name=str(prediction.prediction).replace("_", " "),
            severity=severity,
            confidence_score=Decimal(str(prediction.confidence)),
            treatment_advice=prediction.actions[0],
            prevention_advice="Improve scouting cadence, sanitize tools, and capture follow-up images in 7 days.",
        )
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        return detection

    def _result_payload(self, prediction_key: str, prediction) -> dict:
        return {
            prediction_key: prediction.prediction,
            "confidence_score": prediction.confidence,
            "explanation": prediction.explanation,
            "actions": prediction.actions,
            "metadata": prediction.metadata,
        }

    def _save_recommendation(
        self,
        farm_id,
        zone_id,
        user: User,
        recommendation_type: RecommendationType,
        title: str,
        result: dict,
        input_features: dict,
        confidence_score: Decimal,
    ) -> AIRecommendation:
        recommendation = AIRecommendation(
            farm_id=farm_id,
            zone_id=zone_id,
            user_id=user.id,
            recommendation_type=recommendation_type,
            title=title,
            result=result,
            input_features=input_features,
            confidence_score=confidence_score,
            model_version="baseline-rules-v1",
        )
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation
