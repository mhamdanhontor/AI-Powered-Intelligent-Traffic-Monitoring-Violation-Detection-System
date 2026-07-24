from app.services.yolo_service import model
from app.services.video_processor import VideoProcessor
from app.services.statistics import StatisticsCollector
from app.services.annotator import FrameAnnotator


def detect_vehicles(video_path: str):

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

        stats.update(results, model)

        annotated = FrameAnnotator.draw(results)

        processor.write(annotated)

    processor.release()

    return {
        "statistics": stats.get_statistics(),
        "output_video": str(processor.output_path)
    }