import cv2


class FrameAnnotator:

    @staticmethod
    def draw(results, frame, line_y, speed_estimator):

        annotated = results[0].plot()

        cv2.line(
            annotated,
            (0, line_y),
            (annotated.shape[1], line_y),
            (0, 255, 255),
            3,
        )

        cv2.line(
            annotated,
            (0, speed_estimator.line1),
            (annotated.shape[1], speed_estimator.line1),
            (255, 0, 0),
            2,
        )

        cv2.line(
            annotated,
            (0, speed_estimator.line2),
            (annotated.shape[1], speed_estimator.line2),
            (0, 0, 255),
            2,
        )

        for box in results[0].boxes:

            if box.id is None:
                continue

            track_id = int(box.id)

            if track_id not in speed_estimator.vehicle_speed:
                continue

            x1, y1, x2, y2 = box.xyxy[0]

            cv2.putText(
                annotated,
                f"{speed_estimator.vehicle_speed[track_id]} km/h",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )

        return annotated