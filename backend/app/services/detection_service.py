from app.services.yolo_service import model
from app.services.video_processor import VideoProcessor
from app.services.statistics import StatisticsCollector
from app.services.annotator import FrameAnnotator
from app.services.line_counter import LineCounter

def detect_vehicles(video_path: str):
    counter = LineCounter()
    processor = VideoProcessor(video_path)

    stats = StatisticsCollector()

    while True:

        success, frame = processor.read()

        if not success:
            break

        results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        verbose=False
        )

        counter.update(results)

        stats.update(results, model)

        annotated = FrameAnnotator.draw(

            results,

            frame,

            counter.line_y

        )

        processor.write(annotated)

    processor.release()

    return {

        "statistics": stats.get_statistics(),

        "vehicles_crossed": counter.vehicle_count,

        "output_video": str(processor.output_path)

    }