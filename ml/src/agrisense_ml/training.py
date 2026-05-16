from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from agrisense_ml.config import DATASET_DIR, MODEL_DIR, RANDOM_STATE, REPORT_DIR, ensure_ml_dirs
from agrisense_ml.preprocessing import tabular_preprocessor


def train_crop_model() -> dict:
    numeric = ["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph_level", "rainfall_mm"]
    categorical = ["soil_type"]
    return _train_classifier(
        dataset=DATASET_DIR / "crop_recommendation.csv",
        target="recommended_crop",
        numeric=numeric,
        categorical=categorical,
        estimator=RandomForestClassifier(n_estimators=220, max_depth=12, random_state=RANDOM_STATE, class_weight="balanced"),
        model_name="crop_recommendation.joblib",
        report_name="crop_recommendation_metrics.json",
    )


def train_irrigation_model() -> dict:
    numeric = ["soil_moisture", "temperature", "humidity", "rainfall_forecast_mm", "water_tank_level", "hour_of_day"]
    categorical = ["crop_stage", "soil_type"]
    return _train_classifier(
        dataset=DATASET_DIR / "irrigation_events.csv",
        target="irrigation_action",
        numeric=numeric,
        categorical=categorical,
        estimator=GradientBoostingClassifier(random_state=RANDOM_STATE),
        model_name="irrigation_prediction.joblib",
        report_name="irrigation_prediction_metrics.json",
    )


def train_yield_model() -> dict:
    df = pd.read_csv(DATASET_DIR / "yield_history.csv")
    numeric = ["area_hectares", "rainfall_mm", "avg_temperature", "avg_humidity", "irrigation_events", "fertilizer_score", "soil_health_score"]
    categorical = ["crop_name"]
    x = df[numeric + categorical]
    y = df["yield_tons"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.22, random_state=RANDOM_STATE)
    pipeline = Pipeline(
        steps=[
            ("preprocess", tabular_preprocessor(numeric, categorical)),
            ("model", RandomForestRegressor(n_estimators=260, max_depth=16, random_state=RANDOM_STATE)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    metrics = {
        "model": "RandomForestRegressor",
        "mae": round(float(mean_absolute_error(y_test, predictions)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y_test, predictions))), 4),
        "r2": round(float(r2_score(y_test, predictions)), 4),
        "rows": int(len(df)),
    }
    _save_model_and_metrics(pipeline, "yield_prediction.joblib", metrics, "yield_prediction_metrics.json")
    return metrics


def train_fertilizer_model() -> dict:
    numeric = ["nitrogen", "phosphorus", "potassium", "ph_level"]
    categorical = ["crop_name", "growth_stage", "soil_type"]
    return _train_classifier(
        dataset=DATASET_DIR / "fertilizer_recommendation.csv",
        target="fertilizer_plan",
        numeric=numeric,
        categorical=categorical,
        estimator=RandomForestClassifier(n_estimators=220, max_depth=14, random_state=RANDOM_STATE, class_weight="balanced"),
        model_name="fertilizer_recommendation.joblib",
        report_name="fertilizer_recommendation_metrics.json",
    )


def train_weather_advisory_model() -> dict:
    df = pd.read_csv(DATASET_DIR / "weather_advisory.csv")
    text = df.apply(
        lambda row: (
            f"condition {row.condition} temp {row.temperature:.1f} humidity {row.humidity:.1f} "
            f"rain {row.rainfall_mm:.1f} wind {row.wind_speed:.1f} crop {row.crop_name}"
        ),
        axis=1,
    )
    y = df["suggestion_type"]
    x_train, x_test, y_train, y_test = train_test_split(text, y, test_size=0.22, random_state=RANDOM_STATE, stratify=y)
    pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
            ("model", LogisticRegression(max_iter=800, class_weight="balanced")),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    metrics = _classification_metrics(y_test, predictions, "LogisticRegression+TFIDF", len(df))
    _save_model_and_metrics(pipeline, "weather_advisory.joblib", metrics, "weather_advisory_metrics.json")
    return metrics


def train_disease_model() -> dict:
    numeric = ["leaf_green_index", "spot_ratio", "yellowing_ratio", "texture_score", "edge_damage"]
    categorical = ["crop_name"]
    return _train_classifier(
        dataset=DATASET_DIR / "disease_leaf_features.csv",
        target="disease_name",
        numeric=numeric,
        categorical=categorical,
        estimator=RandomForestClassifier(n_estimators=260, max_depth=12, random_state=RANDOM_STATE, class_weight="balanced"),
        model_name="disease_detection.joblib",
        report_name="disease_detection_metrics.json",
    )


def _train_classifier(dataset: Path, target: str, numeric: list[str], categorical: list[str], estimator, model_name: str, report_name: str) -> dict:
    df = pd.read_csv(dataset)
    x = df[numeric + categorical]
    y = df[target]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.22, random_state=RANDOM_STATE, stratify=y)
    pipeline = Pipeline(
        steps=[
            ("preprocess", tabular_preprocessor(numeric, categorical)),
            ("model", estimator),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    metrics = _classification_metrics(y_test, predictions, estimator.__class__.__name__, len(df))
    _save_model_and_metrics(pipeline, model_name, metrics, report_name)
    return metrics


def _classification_metrics(y_test, predictions, model: str, rows: int) -> dict:
    return {
        "model": model,
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "macro_f1": round(float(f1_score(y_test, predictions, average="macro")), 4),
        "rows": int(rows),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
    }


def _save_model_and_metrics(pipeline, model_name: str, metrics: dict, report_name: str) -> None:
    ensure_ml_dirs()
    joblib.dump(pipeline, MODEL_DIR / model_name)
    (REPORT_DIR / report_name).write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def train_all() -> dict[str, dict]:
    return {
        "crop": train_crop_model(),
        "irrigation": train_irrigation_model(),
        "yield": train_yield_model(),
        "fertilizer": train_fertilizer_model(),
        "weather": train_weather_advisory_model(),
        "disease": train_disease_model(),
    }
