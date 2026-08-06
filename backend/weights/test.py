from ultralytics import YOLO

model = YOLO("backend/weights/helmet.pt")

print(model.names)