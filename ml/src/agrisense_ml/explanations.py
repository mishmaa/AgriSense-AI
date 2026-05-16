from __future__ import annotations


FERTILIZER_EXPLANATIONS = {
    "nitrogen_boost": "Nitrogen appears low for current growth demand, so a nitrogen-forward plan is recommended.",
    "phosphorus_root_support": "Phosphorus support helps root development and flowering performance.",
    "potassium_fruit_support": "Potassium support improves fruit sizing, stress tolerance, and crop quality.",
    "lime_ph_correction": "Soil pH is acidic; lime correction improves nutrient availability.",
    "sulfur_ph_correction": "Soil pH is alkaline; sulfur correction can improve nutrient uptake.",
    "balanced_npk_maintenance": "Nutrient levels are balanced enough for a maintenance NPK program.",
}

IRRIGATION_EXPLANATIONS = {
    "no_irrigation": "Moisture, rainfall, or tank constraints indicate irrigation should be held.",
    "short_cycle": "Moisture is slightly below target, so a short irrigation pulse is enough.",
    "standard_cycle": "Moisture is below the agronomic threshold and needs a normal cycle.",
    "deep_irrigation": "Low moisture combined with heat stress indicates deeper irrigation is justified.",
}

WEATHER_SUGGESTIONS = {
    "delay_irrigation": "Rainfall risk is high. Delay irrigation and protect against runoff.",
    "heat_protection": "Heat stress is likely. Irrigate early, shade sensitive crops, and inspect canopy stress.",
    "fungal_risk": "Humidity and rainfall raise fungal disease risk. Increase scouting and avoid overhead irrigation.",
    "wind_protection": "High wind may damage plants and reduce spray effectiveness. Delay spraying and secure supports.",
    "normal_monitoring": "Weather risk is currently low. Continue normal scouting and sensor monitoring.",
}

DISEASE_TREATMENTS = {
    "healthy": "No visible disease pattern was detected. Continue routine monitoring.",
    "early_blight": "Remove infected leaves, improve airflow, and apply a copper-based fungicide if spread continues.",
    "bacterial_leaf_blight": "Avoid overhead irrigation, remove infected debris, and use disease-free seed next cycle.",
    "northern_leaf_blight": "Scout nearby maize rows, remove severe residue, and consider approved fungicide if humidity remains high.",
    "nutrient_deficiency": "Run a soil test and correct NPK or pH imbalance before adding broad fertilizer.",
    "citrus_canker": "Prune infected material, disinfect tools, and avoid working trees while foliage is wet.",
}


def top_confidence(probabilities: list[float] | None) -> float:
    if not probabilities:
        return 0.7
    return round(float(max(probabilities)), 4)


def crop_explanation(crop: str, features: dict) -> str:
    return (
        f"{crop.title()} matches the supplied NPK balance, pH {features.get('ph_level')}, "
        f"rainfall {features.get('rainfall_mm')} mm, and soil profile."
    )
