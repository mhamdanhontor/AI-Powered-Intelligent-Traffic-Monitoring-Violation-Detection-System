from app.services.yolo_service import (
    vehicle_model,
    helmet_model,
    plate_model,
)

from app.services.helmet_detector import HelmetDetector
from app.services.video_processor import VideoProcessor
from app.services.vehicle_pipeline import VehiclePipeline
from app.services.statistics import StatisticsCollector
from app.services.line_counter import LineCounter
from app.services.speed_estimator import SpeedEstimator
from app.services.trajectory_manager import TrajectoryManager
from app.services.violation_manager import ViolationManager
from app.services.wrong_way_detector import WrongWayDetector
from app.services.annotator import FrameAnnotator
from app.services.plate_detector import PlateDetector
from app.services.ocr_service import OCRService

def detect_vehicles(video_path: str):

    ocr_service = OCRService()

    processor = VideoProcessor(video_path)
    plate_detector = PlateDetector()
    # Vehicle Pipeline
    pipeline = VehiclePipeline(vehicle_model)

    trajectory_manager = TrajectoryManager()

    statistics = StatisticsCollector()

    line_counter = LineCounter()

    speed_estimator = SpeedEstimator(
        fps=processor.fps
    )

    violation_manager = ViolationManager()

    wrong_way_detector = WrongWayDetector(
        violation_manager=violation_manager
    )

    helmet_detector = HelmetDetector(
    helmet_model=helmet_model,
    violation_manager=violation_manager,
    )

    frame_number = 0

    while True:

        success, frame = processor.read()

        if not success:
            break

        frame_number += 1

        # ------------------------------------------
        # Vehicle Detection + Tracking
        # ------------------------------------------

        vehicle_results = vehicle_model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False,
        )

        # ------------------------------------------
        # Plate Detection
        # ------------------------------------------

        plate_results = plate_model.predict(
            frame,
            verbose=False,
        )

        # ------------------------------------------
        # Build Vehicle Objects
        # ------------------------------------------

        vehicles = pipeline.build(
            vehicle_results,
            frame_number,
        )

        # ------------------------------------------
        # Analytics
        # ------------------------------------------

        for vehicle in vehicles:

            trajectory_manager.update(vehicle)

            statistics.update(vehicle)

            line_counter.update(vehicle)

            speed_estimator.update(vehicle)

            violation_manager.add_overspeed(vehicle)

            wrong_way_detector.update(vehicle)

        # ------------------------------------------
        # Helmet Detection
        # ------------------------------------------

        helmet_detector.update(
            frame,
            vehicles,
        )

        # ------------------------------------------
        # Plate Detection
        # ------------------------------------------

        plate_detector.update(
            frame,
            vehicles,
            plate_results,
        )

        for vehicle in vehicles:

            if vehicle.plate_detected:

                vehicle.plate_text = ocr_service.read_plate(
                    vehicle.plate_crop
                )

        # ------------------------------------------
        # Draw
        # ------------------------------------------

        annotated = FrameAnnotator.draw(
            frame=frame,
            results=vehicle_results,
            vehicles=vehicles,
            line_counter=line_counter,
            speed_estimator=speed_estimator,
        )

        processor.write(annotated)

    processor.release()
    violation_manager.save_to_database()
    return {
        "statistics": statistics.get_statistics(),
        "vehicles_crossed": line_counter.vehicle_count,
        "speed_estimation": speed_estimator.vehicle_speed,
        "violations": violation_manager.get_all(),
        "output_video": str(processor.output_path),
    }