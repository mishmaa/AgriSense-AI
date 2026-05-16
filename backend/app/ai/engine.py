import sys
from pathlib import Path


ML_SRC = Path(__file__).resolve().parents[3] / "ml" / "src"
if ML_SRC.exists() and str(ML_SRC) not in sys.path:
    sys.path.append(str(ML_SRC))

from agrisense_ml.predictors import AgriSensePredictor, PredictionResult


class AgriSenseAIEngine:
    def __init__(self) -> None:
        self.predictor = AgriSensePredictor()

    def recommend_crop(self, features: dict) -> PredictionResult:
        return self.predictor.crop(features)

    def predict_irrigation(self, features: dict) -> PredictionResult:
        return self.predictor.irrigation(features)

    def predict_yield(self, features: dict) -> PredictionResult:
        return self.predictor.yield_prediction(features)

    def recommend_fertilizer(self, features: dict) -> PredictionResult:
        return self.predictor.fertilizer(features)

    def suggest_weather_actions(self, features: dict) -> PredictionResult:
        return self.predictor.weather(features)

    def detect_disease(self, features: dict) -> PredictionResult:
        return self.predictor.disease(features)

    def chatbot_reply(self, message: str, context: dict | None = None) -> PredictionResult:
        return self.predictor.chatbot(message, context)


ai_engine = AgriSenseAIEngine()
