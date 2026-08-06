from pathlib import Path

from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parents[2]

WEIGHTS_DIR = BASE_DIR / "weights"

# --------------------------------------------------------
# Vehicle Detection
# --------------------------------------------------------

vehicle_model = YOLO(
    str(
        WEIGHTS_DIR / "yolo11n.pt"
    )
)

# --------------------------------------------------------
# Helmet Detection
# --------------------------------------------------------

helmet_model = YOLO(
    str(
        WEIGHTS_DIR / "helmet.pt"
    )
)

# --------------------------------------------------------
# Number Plate Detection
# --------------------------------------------------------

plate_model = YOLO(
    str(
        WEIGHTS_DIR / "license_plate.pt"
    )
)