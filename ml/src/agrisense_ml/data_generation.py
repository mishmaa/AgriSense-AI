from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd

from agrisense_ml.config import DATASET_DIR, RANDOM_STATE, ensure_ml_dirs


SOIL_TYPES = ["loam", "clay", "sandy", "silt", "peaty"]
CROPS = ["rice", "maize", "tomato", "soybean", "lettuce", "citrus", "wheat"]
GROWTH_STAGES = ["seedling", "vegetative", "flowering", "fruiting", "harvest"]


def generate_all(output_dir: Path = DATASET_DIR, rows: int = 1200) -> dict[str, Path]:
    ensure_ml_dirs()
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "crop": output_dir / "crop_recommendation.csv",
        "irrigation": output_dir / "irrigation_events.csv",
        "yield": output_dir / "yield_history.csv",
        "fertilizer": output_dir / "fertilizer_recommendation.csv",
        "weather": output_dir / "weather_advisory.csv",
        "disease": output_dir / "disease_leaf_features.csv",
    }
    generate_crop_dataset(rows).to_csv(paths["crop"], index=False)
    generate_irrigation_dataset(rows).to_csv(paths["irrigation"], index=False)
    generate_yield_dataset(rows).to_csv(paths["yield"], index=False)
    generate_fertilizer_dataset(rows).to_csv(paths["fertilizer"], index=False)
    generate_weather_dataset(rows).to_csv(paths["weather"], index=False)
    generate_disease_dataset(rows).to_csv(paths["disease"], index=False)
    return paths


def generate_crop_dataset(rows: int) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE)
    data = []
    for _ in range(rows):
        nitrogen = np.clip(rng.normal(70, 28), 10, 145)
        phosphorus = np.clip(rng.normal(48, 18), 8, 95)
        potassium = np.clip(rng.normal(62, 24), 12, 130)
        temperature = np.clip(rng.normal(27, 5), 12, 40)
        humidity = np.clip(rng.normal(68, 16), 25, 95)
        ph_level = np.clip(rng.normal(6.5, 0.9), 4.5, 8.6)
        rainfall = np.clip(rng.normal(105, 55), 5, 280)
        soil_type = random.choice(SOIL_TYPES)
        crop = _select_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph_level, rainfall, soil_type)
        data.append([nitrogen, phosphorus, potassium, temperature, humidity, ph_level, rainfall, soil_type, crop])
    return pd.DataFrame(data, columns=["nitrogen", "phosphorus", "potassium", "temperature", "humidity", "ph_level", "rainfall_mm", "soil_type", "recommended_crop"])


def _select_crop(n, p, k, temp, humidity, ph, rainfall, soil):
    if rainfall > 145 and humidity > 70 and temp > 22:
        return "rice"
    if n > 85 and 5.8 <= ph <= 7.5 and temp >= 24:
        return "maize"
    if p > 50 and 5.8 <= ph <= 7.2 and rainfall < 125:
        return "tomato"
    if n < 65 and soil in {"loam", "silt"}:
        return "soybean"
    if temp < 24 and humidity > 55:
        return "lettuce"
    if k > 78 and ph > 6:
        return "citrus"
    return "wheat"


def generate_irrigation_dataset(rows: int) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE + 1)
    data = []
    for _ in range(rows):
        moisture = rng.uniform(18, 82)
        temp = rng.uniform(18, 39)
        humidity = rng.uniform(35, 94)
        rain = np.clip(rng.exponential(9), 0, 65)
        tank = rng.uniform(8, 100)
        stage = random.choice(GROWTH_STAGES)
        soil = random.choice(SOIL_TYPES)
        hour = int(rng.integers(0, 24))
        if tank < 15 or rain > 25 or moisture > 62:
            action = "no_irrigation"
        elif moisture < 28 and temp > 31:
            action = "deep_irrigation"
        elif moisture < 38:
            action = "standard_cycle"
        else:
            action = "short_cycle"
        data.append([moisture, temp, humidity, rain, tank, stage, soil, hour, action])
    return pd.DataFrame(data, columns=["soil_moisture", "temperature", "humidity", "rainfall_forecast_mm", "water_tank_level", "crop_stage", "soil_type", "hour_of_day", "irrigation_action"])


def generate_yield_dataset(rows: int) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE + 2)
    crop_base = {"rice": 4.9, "maize": 5.6, "tomato": 38, "soybean": 2.8, "lettuce": 22, "citrus": 16, "wheat": 3.6}
    data = []
    for _ in range(rows):
        crop = random.choice(CROPS)
        area = rng.uniform(0.4, 55)
        rainfall = rng.uniform(20, 240)
        temp = rng.uniform(16, 36)
        humidity = rng.uniform(35, 92)
        irrigation_events = int(rng.integers(4, 80))
        fertilizer_score = rng.uniform(0.35, 1.0)
        soil_health = rng.uniform(0.45, 1.0)
        stress_penalty = max(0, abs(temp - 27) - 5) * 0.04
        water_bonus = min(rainfall / 140, 1.25) * 0.12
        yield_per_hectare = crop_base[crop] * (0.58 + fertilizer_score * 0.22 + soil_health * 0.18 + water_bonus - stress_penalty)
        yield_tons = max(0.2, area * yield_per_hectare + rng.normal(0, area * 0.08))
        data.append([crop, area, rainfall, temp, humidity, irrigation_events, fertilizer_score, soil_health, yield_tons])
    return pd.DataFrame(data, columns=["crop_name", "area_hectares", "rainfall_mm", "avg_temperature", "avg_humidity", "irrigation_events", "fertilizer_score", "soil_health_score", "yield_tons"])


def generate_fertilizer_dataset(rows: int) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE + 3)
    data = []
    for _ in range(rows):
        crop = random.choice(CROPS)
        stage = random.choice(GROWTH_STAGES)
        soil = random.choice(SOIL_TYPES)
        n = rng.uniform(15, 135)
        p = rng.uniform(8, 90)
        k = rng.uniform(15, 135)
        ph = rng.uniform(4.8, 8.4)
        if n < 45:
            plan = "nitrogen_boost"
        elif p < 28 and stage in {"seedling", "flowering"}:
            plan = "phosphorus_root_support"
        elif k < 42 and crop in {"tomato", "citrus"}:
            plan = "potassium_fruit_support"
        elif ph < 5.7:
            plan = "lime_ph_correction"
        elif ph > 7.8:
            plan = "sulfur_ph_correction"
        else:
            plan = "balanced_npk_maintenance"
        data.append([crop, stage, soil, n, p, k, ph, plan])
    return pd.DataFrame(data, columns=["crop_name", "growth_stage", "soil_type", "nitrogen", "phosphorus", "potassium", "ph_level", "fertilizer_plan"])


def generate_weather_dataset(rows: int) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE + 4)
    conditions = ["clear", "partly_cloudy", "light_rain", "heavy_rain", "hot", "windy", "humid"]
    data = []
    for _ in range(rows):
        crop = random.choice(CROPS)
        condition = random.choice(conditions)
        temp = rng.uniform(14, 41)
        humidity = rng.uniform(30, 96)
        rainfall = np.clip(rng.exponential(12), 0, 90)
        wind = rng.uniform(1, 45)
        if rainfall > 35:
            suggestion = "delay_irrigation"
        elif temp > 34:
            suggestion = "heat_protection"
        elif humidity > 82 and rainfall > 12:
            suggestion = "fungal_risk"
        elif wind > 30:
            suggestion = "wind_protection"
        else:
            suggestion = "normal_monitoring"
        data.append([condition, temp, humidity, rainfall, wind, crop, suggestion])
    return pd.DataFrame(data, columns=["condition", "temperature", "humidity", "rainfall_mm", "wind_speed", "crop_name", "suggestion_type"])


def generate_disease_dataset(rows: int) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_STATE + 5)
    data = []
    for _ in range(rows):
        crop = random.choice(["tomato", "maize", "rice", "citrus"])
        green = rng.uniform(0.25, 0.92)
        spot = rng.uniform(0, 0.58)
        yellow = rng.uniform(0, 0.65)
        texture = rng.uniform(0.18, 0.96)
        edge = rng.uniform(0, 0.7)
        if spot > 0.34 and crop == "tomato":
            disease = "early_blight"
        elif yellow > 0.42 and crop == "rice":
            disease = "bacterial_leaf_blight"
        elif edge > 0.46 and crop == "maize":
            disease = "northern_leaf_blight"
        elif green < 0.42 and yellow > 0.32:
            disease = "nutrient_deficiency"
        elif spot > 0.38 and crop == "citrus":
            disease = "citrus_canker"
        else:
            disease = "healthy"
        data.append([crop, green, spot, yellow, texture, edge, disease])
    return pd.DataFrame(data, columns=["crop_name", "leaf_green_index", "spot_ratio", "yellowing_ratio", "texture_score", "edge_damage", "disease_name"])
