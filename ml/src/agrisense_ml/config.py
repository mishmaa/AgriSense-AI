from pathlib import Path


ML_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = ML_ROOT / "datasets"
MODEL_DIR = ML_ROOT / "models"
REPORT_DIR = ML_ROOT / "reports"

RANDOM_STATE = 42


def ensure_ml_dirs() -> None:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
