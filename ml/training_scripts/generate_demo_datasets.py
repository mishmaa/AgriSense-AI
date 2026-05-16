import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from agrisense_ml.data_generation import generate_all


if __name__ == "__main__":
    paths = generate_all()
    for name, path in paths.items():
        print(f"{name}: {path}")
