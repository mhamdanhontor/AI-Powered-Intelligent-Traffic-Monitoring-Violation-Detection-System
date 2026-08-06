import cv2


class FrameAnnotator:

    @staticmethod
    def draw(
        frame,
        results,
        vehicles,
        line_counter,
        speed_estimator,
    ):
        """
        Draw everything on the frame.

        - YOLO detections
        - Counting line
        - Speed lines
        - Vehicle speed
        - Wrong-way warning
        """

        annotated = results[0].plot()

        # --------------------------------------------------
        # Counting Line
        # --------------------------------------------------
        cv2.line(
            annotated,
            (0, line_counter.line_y),
            (annotated.shape[1], line_counter.line_y),
            (0, 255, 255),
            3,
        )

        # --------------------------------------------------
        # Speed Estimation Lines
        # --------------------------------------------------
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

        # --------------------------------------------------
        # Draw Vehicle Information
        # --------------------------------------------------
        for vehicle in vehicles:

            x1 = int(vehicle.x1)
            y1 = int(vehicle.y1)

            # --------------------------------------------------
            # Speed
            # --------------------------------------------------

            if vehicle.speed is not None:

                cv2.putText(
                    annotated,
                    f"{vehicle.speed:.1f} km/h",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )
            if vehicle.overspeed:

                cv2.putText(
                    annotated,
                    "OVERSPEED",
                    (x1, y1 - 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )
            # --------------------------------------------------
            # Helmet Status
            # --------------------------------------------------

            if vehicle.has_helmet is True:

                cv2.putText(
                    annotated,
                    "Helmet",
                    (x1, y1 - 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )

            elif vehicle.has_helmet is False:

                cv2.putText(
                    annotated,
                    "NO HELMET",
                    (x1, y1 - 55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            # --------------------------------------------------
            # Wrong Way
            # --------------------------------------------------

            if vehicle.wrong_way:

                cv2.putText(
                    annotated,
                    "WRONG WAY",
                    (x1, y1 - 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    3,
                )

                cv2.rectangle(
                    annotated,
                    (int(vehicle.x1), int(vehicle.y1)),
                    (int(vehicle.x2), int(vehicle.y2)),
                    (0, 0, 255),
                    3,
                )

            # --------------------------------------------------
            # Plate Detection
            # --------------------------------------------------

            if vehicle.plate_detected and vehicle.plate_bbox is not None:

                px1, py1, px2, py2 = vehicle.plate_bbox

                cv2.rectangle(
                    annotated,
                    (px1, py1),
                    (px2, py2),
                    (255, 255, 0),
                    2,
                )

                cv2.putText(
                    annotated,
                    "Plate",
                    (px1, py1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 0),
                    2,
                )

                if vehicle.plate_text:

                    cv2.putText(
                        annotated,
                        vehicle.plate_text,
                        (px1, py2 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 0),
                        2,
                    )

        # --------------------------------------------------
        # Vehicle Counter
        # --------------------------------------------------
        cv2.putText(
            annotated,
            f"Vehicles : {line_counter.vehicle_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        return annotated