from typing import List

from app.services.vehicle import Vehicle


class VehiclePipeline:
    """
    Converts raw YOLO tracking results into Vehicle objects.

    Every frame:
        YOLO Results
              ↓
        Vehicle Objects
              ↓
        Detection Pipeline
    """

    def __init__(self, model):
        self.model = model

    def build(self, results, frame_number: int) -> List[Vehicle]:

        vehicles = []

        names = self.model.names

        for box in results[0].boxes:

            if box.id is None:
                continue

            track_id = int(box.id)

            class_id = int(box.cls[0])

            class_name = names[class_id]

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            vehicle = Vehicle(
                track_id=track_id,
                class_id=class_id,
                class_name=class_name,
                confidence=confidence,
                bbox=(x1, y1, x2, y2),
                center=(center_x, center_y),
                frame_number=frame_number
            )

            vehicles.append(vehicle)

        return vehicles