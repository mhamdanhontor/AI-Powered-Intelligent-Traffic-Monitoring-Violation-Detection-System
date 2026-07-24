from ultralytics import YOLO
from app.config import WEIGHTS_FOLDER

MODEL_PATH = WEIGHTS_FOLDER / "yolo11n.pt"

model = YOLO(str(MODEL_PATH))