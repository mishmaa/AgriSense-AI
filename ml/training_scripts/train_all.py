import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from agrisense_ml.data_generation import generate_all
from agrisense_ml.training import train_all


if __name__ == "__main__":
    generate_all()
    metrics = train_all()
    print(json.dumps(metrics, indent=2))
