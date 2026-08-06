import cv2
from uuid import uuid4

from app.config import OUTPUT_FOLDER


class VideoProcessor:
    """
    Handles all video input/output operations.

    Responsibilities:
    - Open input video
    - Read frames
    - Write output video
    - Store video metadata (FPS, width, height, frame count)
    """

    def __init__(self, video_path: str):

        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise Exception(f"Unable to open video: {video_path}")

        # -----------------------------
        # Video Properties
        # -----------------------------
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

        # Some videos return 0 FPS
        if self.fps is None or self.fps <= 0:
            self.fps = 30.0

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # -----------------------------
        # Output Video
        # -----------------------------
        self.output_path = OUTPUT_FOLDER / f"{uuid4().hex}.mp4"

        self.writer = cv2.VideoWriter(
            str(self.output_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            self.fps,
            (self.width, self.height),
        )

        self.current_frame = 0

    def read(self):
        """
        Read one frame from the video.
        """

        success, frame = self.cap.read()

        if success:
            self.current_frame += 1

        return success, frame

    def write(self, frame):
        """
        Write one frame to the output video.
        """

        self.writer.write(frame)

    def is_open(self):
        """
        Check whether the video is still open.
        """

        return self.cap.isOpened()

    def get_progress(self):
        """
        Returns processing progress as a percentage.
        """

        if self.total_frames == 0:
            return 0.0

        return (self.current_frame / self.total_frames) * 100

    def release(self):
        """
        Release all resources.
        """

        if self.cap is not None:
            self.cap.release()

        if self.writer is not None:
            self.writer.release()

        cv2.destroyAllWindows()