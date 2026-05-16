# AgriSense AI Machine Learning Architecture

This ML layer gives AgriSense AI trainable models, explainable predictions, confidence scores, evaluation metrics, and backend integration points. The implementation is intentionally lightweight enough for a university final-year project while keeping the structure close to a commercial ML service.

## 1. ML Architecture

```txt
ml/
├── datasets/
│   ├── crop_recommendation.csv
│   ├── irrigation_events.csv
│   ├── yield_history.csv
│   ├── fertilizer_recommendation.csv
│   ├── weather_advisory.csv
│   └── disease_leaf_features.csv
├── models/
│   └── *.joblib
├── reports/
│   └── *_metrics.json
├── src/agrisense_ml/
│   ├── config.py
│   ├── data_generation.py
│   ├── preprocessing.py
│   ├── predictors.py
│   └── explanations.py
└── training_scripts/
    ├── generate_demo_datasets.py
    ├── train_all.py
    ├── train_crop_model.py
    ├── train_irrigation_model.py
    ├── train_yield_model.py
    ├── train_fertilizer_model.py
    ├── train_weather_advisory_model.py
    └── train_disease_model.py
```

The backend imports `agrisense_ml.predictors`. If trained `.joblib` files exist, the backend uses them. If they are missing, the predictor layer uses deterministic agronomy fallbacks so the API remains demoable.

## 2. Algorithms Used

| Feature | Algorithm | Why selected |
| --- | --- | --- |
| Crop recommendation | Random Forest Classifier | Handles nonlinear NPK, pH, rainfall, soil, and climate interactions; robust on small tabular datasets. |
| Irrigation prediction | Gradient Boosting Classifier | Strong tabular classifier for threshold-like decisions with weather and moisture interactions. |
| Yield prediction | Random Forest Regressor | Captures nonlinear effects between area, weather, irrigation frequency, fertilizer score, and crop type. |
| Fertilizer recommendation | Random Forest Classifier | Multi-class recommendation over nutrient imbalance, crop, soil, and growth stage. |
| Weather suggestions | Logistic Regression with TF-IDF | Interpretable text/category baseline for advisory classification. |
| Plant disease detection | Random Forest Classifier over extracted leaf features | Lightweight stand-in for CNN image classification; can be replaced with TensorFlow/PyTorch transfer learning. |
| Farming chatbot | Retrieval + intent classifier rules | Reliable offline demo assistant with scoped agriculture responses. |

## 3. Dataset Structure

### Crop recommendation

Features:

- `nitrogen`, `phosphorus`, `potassium`
- `temperature`, `humidity`, `ph_level`, `rainfall_mm`
- `soil_type`

Target:

- `recommended_crop`

### Irrigation prediction

Features:

- `soil_moisture`, `temperature`, `humidity`, `rainfall_forecast_mm`
- `water_tank_level`, `crop_stage`, `soil_type`, `hour_of_day`

Target:

- `irrigation_action`: `no_irrigation`, `short_cycle`, `standard_cycle`, `deep_irrigation`

### Yield prediction

Features:

- `crop_name`, `area_hectares`, `rainfall_mm`, `avg_temperature`
- `avg_humidity`, `irrigation_events`, `fertilizer_score`, `soil_health_score`

Target:

- `yield_tons`

### Fertilizer recommendation

Features:

- `crop_name`, `growth_stage`, `soil_type`, `nitrogen`, `phosphorus`, `potassium`, `ph_level`

Target:

- `fertilizer_plan`

### Weather advisory

Features:

- `condition`, `temperature`, `humidity`, `rainfall_mm`, `wind_speed`, `crop_name`

Target:

- `suggestion_type`: `delay_irrigation`, `heat_protection`, `fungal_risk`, `normal_monitoring`, `wind_protection`

### Disease detection

Features:

- `crop_name`, `leaf_green_index`, `spot_ratio`, `yellowing_ratio`, `texture_score`, `edge_damage`

Target:

- `disease_name`

For production, replace these demo features with CNN embeddings from uploaded leaf images.

## 4. Training Workflow

1. Generate or collect datasets in `ml/datasets`.
2. Run `python training_scripts/generate_demo_datasets.py`.
3. Run `python training_scripts/train_all.py`.
4. Each training script builds a scikit-learn `Pipeline` with preprocessing and model steps.
5. Metrics are saved to `ml/reports`.
6. Trained models are saved to `ml/models`.
7. Backend APIs call `app.ai.engine.AgriSenseAIEngine`.

## 5. Preprocessing Pipelines

- Numeric features: median imputation and standard scaling.
- Categorical features: most-frequent imputation and one-hot encoding.
- Text advisory features: template text generation followed by TF-IDF.
- All pipelines are serialized with the model so prediction preprocessing matches training preprocessing.

## 6. Evaluation Metrics

| Task | Metrics |
| --- | --- |
| Classification | Accuracy, macro F1, classification report |
| Regression | MAE, RMSE, R2 |
| Advisory/chatbot | Intent coverage, qualitative response accuracy |

Expected demo metrics on generated datasets typically land around:

- Crop recommendation accuracy: 0.85-0.95
- Irrigation action accuracy: 0.82-0.92
- Fertilizer recommendation accuracy: 0.80-0.90
- Disease feature classifier accuracy: 0.78-0.88
- Yield prediction R2: 0.80-0.92

Actual values are written to `ml/reports` after training.

## 7. Prediction APIs

Backend endpoints:

```txt
POST /api/v1/ai/crop-recommendation
POST /api/v1/ai/fertilizer-recommendation
POST /api/v1/ai/yield-prediction
POST /api/v1/ai/irrigation-prediction
POST /api/v1/ai/weather-suggestion
POST /api/v1/disease-detection
POST /api/v1/chatbot/message
```

All AI responses include:

- prediction or recommendation
- confidence score
- model version
- input features
- explanation
- recommended actions

## 8. Model Explanations

The current implementation uses practical explanation templates based on:

- strongest feature drivers
- threshold interpretation
- predicted class confidence
- agronomy rules tied to the model output

Future upgrades can add SHAP values for tabular models and Grad-CAM heatmaps for disease detection.

## 9. Future Improvements

- Replace synthetic datasets with Kaggle, government agriculture, university trial, and local farm datasets.
- Add TensorFlow/PyTorch CNN transfer learning for leaf disease images.
- Add SHAP model explanations for crop, fertilizer, and irrigation models.
- Add MLflow or Weights & Biases experiment tracking.
- Add model registry, drift monitoring, and scheduled retraining.
- Add RAG chatbot with agriculture manuals, weather APIs, and farm history.
- Add geospatial satellite/drone imagery models for NDVI and crop stress.
