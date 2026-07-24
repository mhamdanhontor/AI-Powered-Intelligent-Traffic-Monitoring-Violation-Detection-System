import cv2
from uuid import uuid4

from app.config import OUTPUT_FOLDER


class VideoProcessor:

    def __init__(self, video_path):

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise Exception("Unable to open video.")

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.output_path = OUTPUT_FOLDER / f"{uuid4().hex}.mp4"

        self.writer = cv2.VideoWriter(
            str(self.output_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

    def read(self):

        return self.cap.read()

    def write(self, frame):

        self.writer.write(frame)

    def release(self):

        self.cap.release()
        self.writer.release()