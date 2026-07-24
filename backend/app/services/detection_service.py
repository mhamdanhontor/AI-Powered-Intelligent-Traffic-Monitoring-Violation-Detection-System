import cv2
from uuid import uuid4
from app.services.yolo_service import model
from app.config import OUTPUT_FOLDER


def detect_vehicles(video_path: str):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Unable to open video.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = OUTPUT_FOLDER / f"{uuid4().hex}.mp4"

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    vehicle_stats = {
        "car": 0,
        "truck": 0,
        "bus": 0,
        "motorcycle": 0,
    }

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Run YOLO
        results = model(frame)

        # Count detected vehicles
        for box in results[0].boxes:

            class_id = int(box.cls)
            class_name = model.names[class_id]

            if class_name in vehicle_stats:
                vehicle_stats[class_name] += 1

        # Draw bounding boxes
        annotated_frame = results[0].plot()

        # Save frame
        writer.write(annotated_frame)

    cap.release()
    writer.release()

    return {
        "statistics": vehicle_stats,
        "output_video": str(output_path)
    }