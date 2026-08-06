import cv2


class PlateDetector:

    """
    Detect and associate licence plates with tracked vehicles.
    """

    def __init__(self):

        self.supported_classes = {
            "car",
            "truck",
            "bus",
            "motorcycle",
            "motorbike",
        }

    def update(
        self,
        frame,
        vehicles,
        plate_results,
    ):

        if len(plate_results) == 0:
            return

        boxes = plate_results[0].boxes

        for vehicle in vehicles:

            vehicle.plate_detected = False
            vehicle.plate_bbox = None
            vehicle.plate_confidence = None
            vehicle.plate_crop = None

            if vehicle.class_name.lower() not in self.supported_classes:
                continue

            best_conf = 0

            best_box = None

            for box in boxes:

                px1, py1, px2, py2 = box.xyxy[0]

                cx = (px1 + px2) / 2
                cy = (py1 + py2) / 2

                if (
                    vehicle.x1 <= cx <= vehicle.x2
                    and vehicle.y1 <= cy <= vehicle.y2
                ):

                    conf = float(box.conf[0])

                    if conf > best_conf:

                        best_conf = conf

                        best_box = (
                            int(px1),
                            int(py1),
                            int(px2),
                            int(py2),
                        )

            if best_box is None:
                continue

            vehicle.plate_detected = True

            vehicle.plate_confidence = best_conf

            vehicle.plate_bbox = best_box

            px1, py1, px2, py2 = best_box

            h, w = frame.shape[:2]

            px1 = max(0, px1)
            py1 = max(0, py1)
            px2 = min(w, px2)
            py2 = min(h, py2)

            vehicle.plate_crop = frame[
                py1:py2,
                px1:px2,
            ].copy()