import cv2


class HelmetDetector:
    """
    Detect helmet status by running the helmet model
    only on motorcycle/bicycle crops.
    """

    def __init__(self, helmet_model, violation_manager):

        self.helmet_model = helmet_model
        self.violation_manager = violation_manager

        self.vehicle_classes = {
            "motorcycle",
            "motorbike",
            "bicycle",
        }

        self.reported = set()

    def update(self, frame, vehicles):

        for vehicle in vehicles:

            if vehicle.class_name.lower() not in self.vehicle_classes:
                continue

            vehicle.has_helmet = None
            vehicle.helmet_confidence = None

            x1 = max(0, int(vehicle.x1))
            y1 = max(0, int(vehicle.y1))
            x2 = min(frame.shape[1], int(vehicle.x2))
            y2 = min(frame.shape[0], int(vehicle.y2))

            if x2 <= x1 or y2 <= y1:
                continue

            roi = frame[y1:y2, x1:x2]

            if roi.size == 0:
                continue

            results = self.helmet_model.predict(
                roi,
                verbose=False,
            )

            if len(results) == 0:
                continue

            boxes = results[0].boxes

            if len(boxes) == 0:

                vehicle.has_helmet = False

                self.add_violation(vehicle)

                continue

            best_box = max(
                boxes,
                key=lambda b: float(b.conf[0])
            )

            cls = int(best_box.cls[0])
            conf = float(best_box.conf[0])

            vehicle.helmet_confidence = conf

            # Model classes:
            # 0 = helmet
            # 1 = face (no helmet)

            if cls == 0:

                vehicle.has_helmet = True

                self.remove_violation(vehicle)

            else:

                vehicle.has_helmet = False

                self.add_violation(vehicle)

    def add_violation(self, vehicle):

        if vehicle.track_id in self.reported:
            return

        self.reported.add(vehicle.track_id)

        self.violation_manager.add_violation(
            violation_type="no_helmet",
            track_id=vehicle.track_id,
            vehicle_type=vehicle.class_name,
            frame_number=vehicle.frame_number,
            confidence=vehicle.helmet_confidence or 1.0,
            metadata={
                "helmet": False,
            },
        )

    def remove_violation(self, vehicle):

        if vehicle.track_id not in self.reported:
            return

        self.reported.remove(vehicle.track_id)

        self.violation_manager.remove_violation(
            "no_helmet",
            vehicle.track_id,
        )