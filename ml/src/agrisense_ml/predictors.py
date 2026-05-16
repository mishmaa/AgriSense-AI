from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from agrisense_ml.config import MODEL_DIR
from agrisense_ml.explanations import (
    DISEASE_TREATMENTS,
    FERTILIZER_EXPLANATIONS,
    IRRIGATION_EXPLANATIONS,
    WEATHER_SUGGESTIONS,
    crop_explanation,
    top_confidence,
)


@dataclass
class PredictionResult:
    prediction: str | float
    confidence: float
    explanation: str
    model_version: str
    actions: list[str]
    metadata: dict[str, Any]


class AgriSensePredictor:
    def __init__(self, model_dir: Path = MODEL_DIR):
        self.model_dir = model_dir
        self.models: dict[str, Any] = {}

    def crop(self, features: dict[str, Any]) -> PredictionResult:
        model = self._load("crop", "crop_recommendation.joblib")
        if model:
            prediction, confidence = self._predict_class(model, features)
        else:
            prediction = self._fallback_crop(features)
            confidence = 0.72
        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            explanation=crop_explanation(str(prediction), features),
            model_version=self._version(model, "crop-rules-v1"),
            actions=[
                f"Validate {str(prediction).title()} against local market demand.",
                "Run a soil test before planting.",
                "Review irrigation capacity for the selected crop.",
            ],
            metadata={"input_features": features},
        )

    def irrigation(self, features: dict[str, Any]) -> PredictionResult:
        model = self._load("irrigation", "irrigation_prediction.joblib")
        if model:
            prediction, confidence = self._predict_class(model, features)
        else:
            prediction = self._fallback_irrigation(features)
            confidence = 0.7
        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            explanation=IRRIGATION_EXPLANATIONS.get(str(prediction), "Irrigation decision generated from current farm signals."),
            model_version=self._version(model, "irrigation-rules-v1"),
            actions=self._irrigation_actions(str(prediction)),
            metadata={"input_features": features},
        )

    def yield_prediction(self, features: dict[str, Any]) -> PredictionResult:
        model = self._load("yield", "yield_prediction.joblib")
        if model:
            frame = pd.DataFrame([features])
            prediction = float(model.predict(frame)[0])
            confidence = 0.78
        else:
            prediction = self._fallback_yield(features)
            confidence = 0.68
        return PredictionResult(
            prediction=round(prediction, 2),
            confidence=confidence,
            explanation="Yield estimate combines crop type, farm area, weather, irrigation, fertilizer, and soil health signals.",
            model_version=self._version(model, "yield-rules-v1"),
            actions=[
                "Compare predicted yield with historical farm average.",
                "Improve fertilizer score and irrigation consistency to raise the forecast.",
            ],
            metadata={
                "input_features": features,
                "confidence_interval": [round(prediction * 0.88, 2), round(prediction * 1.12, 2)],
            },
        )

    def fertilizer(self, features: dict[str, Any]) -> PredictionResult:
        model = self._load("fertilizer", "fertilizer_recommendation.joblib")
        if model:
            prediction, confidence = self._predict_class(model, features)
        else:
            prediction = self._fallback_fertilizer(features)
            confidence = 0.7
        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            explanation=FERTILIZER_EXPLANATIONS.get(str(prediction), "Fertilizer plan generated from nutrient balance and crop stage."),
            model_version=self._version(model, "fertilizer-rules-v1"),
            actions=[
                "Apply in split doses where possible.",
                "Avoid fertilizing immediately before heavy rain.",
                "Retest soil after the next growth stage.",
            ],
            metadata={"input_features": features},
        )

    def weather(self, features: dict[str, Any]) -> PredictionResult:
        model = self._load("weather", "weather_advisory.joblib")
        text = self._weather_text(features)
        if model:
            prediction, confidence = self._predict_text_class(model, text)
        else:
            prediction = self._fallback_weather(features)
            confidence = 0.72
        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            explanation=WEATHER_SUGGESTIONS.get(str(prediction), "Weather advisory generated from forecast risk."),
            model_version=self._version(model, "weather-rules-v1"),
            actions=[WEATHER_SUGGESTIONS.get(str(prediction), "Continue monitoring weather and sensor conditions.")],
            metadata={"input_features": features, "advisory_text": text},
        )

    def disease(self, features: dict[str, Any]) -> PredictionResult:
        model = self._load("disease", "disease_detection.joblib")
        if model:
            prediction, confidence = self._predict_class(model, features)
        else:
            prediction = self._fallback_disease(features)
            confidence = 0.69
        return PredictionResult(
            prediction=prediction,
            confidence=confidence,
            explanation=f"{str(prediction).replace('_', ' ').title()} detected from crop and leaf feature signals.",
            model_version=self._version(model, "disease-rules-v1"),
            actions=[
                DISEASE_TREATMENTS.get(str(prediction), "Scout affected zones and collect another image sample."),
                "Confirm with a local agronomist before chemical treatment.",
            ],
            metadata={"input_features": features},
        )

    def chatbot(self, message: str, context: dict[str, Any] | None = None) -> PredictionResult:
        lowered = message.lower()
        if any(term in lowered for term in ["irrigation", "water", "moisture", "灌溉", "水", "湿度", "آبپاشی", "پانی", "نمی"]):
            intent = "irrigation_advice"
            reply = "Check the latest soil moisture and rainfall forecast. If moisture is below 35% and rain is unlikely, run a targeted drip cycle."
        elif any(term in lowered for term in ["disease", "leaf", "spot", "yellow", "病害", "叶", "斑", "发黄", "بیماری", "پتا", "داغ", "پیلا"]):
            intent = "disease_advice"
            reply = "Use disease detection with a clear leaf image, then isolate affected plants while waiting for confirmation."
        elif any(term in lowered for term in ["fertilizer", "npk", "nitrogen", "肥料", "氮", "磷", "钾", "کھاد", "نائٹروجن"]):
            intent = "fertilizer_advice"
            reply = "Use NPK readings with crop stage. Split applications and avoid fertilizing before heavy rain."
        elif any(term in lowered for term in ["weather", "rain", "heat", "天气", "降雨", "高温", "موسم", "بارش", "گرمی"]):
            intent = "weather_advice"
            reply = "Use weather intelligence to adjust irrigation timing, protect against heat stress, and monitor fungal risk after rain."
        else:
            intent = "general_farming"
            reply = "I can help with crop selection, irrigation, fertilizer planning, disease scouting, yield forecasts, and weather risk."
        return PredictionResult(
            prediction=reply,
            confidence=0.76,
            explanation=f"Matched chatbot intent: {intent}.",
            model_version="retrieval-intent-v1",
            actions=["Ask a follow-up with crop, zone, and latest sensor values for a sharper answer."],
            metadata={"intent": intent, "context": context or {}},
        )

    def _load(self, key: str, filename: str):
        if key in self.models:
            return self.models[key]
        path = self.model_dir / filename
        if not path.exists():
            self.models[key] = None
            return None
        self.models[key] = joblib.load(path)
        return self.models[key]

    def _predict_class(self, model, features: dict[str, Any]) -> tuple[str, float]:
        frame = pd.DataFrame([features])
        prediction = str(model.predict(frame)[0])
        probabilities = model.predict_proba(frame)[0].tolist() if hasattr(model, "predict_proba") else None
        return prediction, top_confidence(probabilities)

    def _predict_text_class(self, model, text: str) -> tuple[str, float]:
        prediction = str(model.predict([text])[0])
        probabilities = model.predict_proba([text])[0].tolist() if hasattr(model, "predict_proba") else None
        return prediction, top_confidence(probabilities)

    def _version(self, model, fallback: str) -> str:
        return "sklearn-pipeline-v1" if model else fallback

    def _weather_text(self, features: dict[str, Any]) -> str:
        return (
            f"condition {features.get('condition')} temp {features.get('temperature')} humidity {features.get('humidity')} "
            f"rain {features.get('rainfall_mm')} wind {features.get('wind_speed')} crop {features.get('crop_name')}"
        )

    def _fallback_crop(self, f: dict[str, Any]) -> str:
        if float(f.get("rainfall_mm", 0)) > 145 and float(f.get("humidity", 0)) > 70:
            return "rice"
        if float(f.get("nitrogen", 0)) > 85:
            return "maize"
        if float(f.get("phosphorus", 0)) > 50:
            return "tomato"
        return "soybean"

    def _fallback_irrigation(self, f: dict[str, Any]) -> str:
        moisture = float(f.get("soil_moisture", 45))
        rain = float(f.get("rainfall_forecast_mm", 0))
        tank = float(f.get("water_tank_level", 70))
        temp = float(f.get("temperature", 28))
        if tank < 15 or rain > 25 or moisture > 62:
            return "no_irrigation"
        if moisture < 28 and temp > 31:
            return "deep_irrigation"
        if moisture < 38:
            return "standard_cycle"
        return "short_cycle"

    def _irrigation_actions(self, prediction: str) -> list[str]:
        return {
            "no_irrigation": ["Pause irrigation and monitor rainfall or tank constraints."],
            "short_cycle": ["Run drip irrigation for 8-12 minutes.", "Recheck moisture after 30 minutes."],
            "standard_cycle": ["Run irrigation for 15-22 minutes.", "Prioritize zones below 38% moisture."],
            "deep_irrigation": ["Run a deep cycle before peak heat.", "Check tank level and avoid runoff."],
        }.get(prediction, ["Review irrigation settings."])

    def _fallback_yield(self, f: dict[str, Any]) -> float:
        return float(f.get("farm_area_hectares", f.get("area_hectares", 1))) * (3.1 + float(f.get("fertilizer_score", 0.65)))

    def _fallback_fertilizer(self, f: dict[str, Any]) -> str:
        if float(f.get("nitrogen", 80)) < 45:
            return "nitrogen_boost"
        if float(f.get("phosphorus", 40)) < 28:
            return "phosphorus_root_support"
        if float(f.get("potassium", 60)) < 42:
            return "potassium_fruit_support"
        if float(f.get("ph_level", 6.5)) < 5.7:
            return "lime_ph_correction"
        return "balanced_npk_maintenance"

    def _fallback_weather(self, f: dict[str, Any]) -> str:
        if float(f.get("rainfall_mm", 0)) > 35:
            return "delay_irrigation"
        if float(f.get("temperature", 25)) > 34:
            return "heat_protection"
        if float(f.get("humidity", 50)) > 82:
            return "fungal_risk"
        if float(f.get("wind_speed", 0)) > 30:
            return "wind_protection"
        return "normal_monitoring"

    def _fallback_disease(self, f: dict[str, Any]) -> str:
        crop = str(f.get("crop_name", "tomato"))
        if float(f.get("spot_ratio", 0)) > 0.34 and crop == "tomato":
            return "early_blight"
        if float(f.get("yellowing_ratio", 0)) > 0.42 and crop == "rice":
            return "bacterial_leaf_blight"
        if float(f.get("edge_damage", 0)) > 0.46 and crop == "maize":
            return "northern_leaf_blight"
        if float(f.get("leaf_green_index", 0.7)) < 0.42:
            return "nutrient_deficiency"
        return "healthy"
