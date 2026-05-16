import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from agrisense_ml.training import train_yield_model


if __name__ == "__main__":
    print(train_yield_model())
