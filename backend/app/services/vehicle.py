from dataclasses import dataclass, field
from typing import Tuple, List, Optional


@dataclass
class Vehicle:
    """
    Represents one tracked vehicle.
    Every detector and analytics module works
    with this object.
    """

    # =====================================================
    # Required Fields (NO DEFAULT VALUES)
    # =====================================================

    track_id: int

    class_id: int

    class_name: str

    confidence: float

    bbox: Tuple[int, int, int, int]

    center: Tuple[int, int]

    frame_number: int

    # =====================================================
    # Trajectory
    # =====================================================

    history: List[Tuple[int, int]] = field(default_factory=list)

    # =====================================================
    # Line Counter
    # =====================================================

    crossed_line: bool = False

    # =====================================================
    # Speed Estimation
    # =====================================================

    speed: Optional[float] = None

    overspeed: bool = False

    # =====================================================
    # Wrong Way Detection
    # =====================================================

    wrong_way: bool = False

    direction: Optional[str] = None

    direction_score: float = 0.0

    # =====================================================
    # Helmet Detection
    # =====================================================

    has_helmet: Optional[bool] = None

    helmet_confidence: Optional[float] = None

    # =====================================================
    # Number Plate Detection
    # =====================================================

    plate_detected: bool = False

    plate_bbox: Optional[Tuple[int, int, int, int]] = None

    plate_confidence: Optional[float] = None

    plate_text: Optional[str] = None

    plate_crop = None

    # =====================================================
    # Extra Metadata
    # =====================================================

    metadata: dict = field(default_factory=dict)

    # =====================================================
    # Bounding Box Helpers
    # =====================================================

    @property
    def x1(self):
        return self.bbox[0]

    @property
    def y1(self):
        return self.bbox[1]

    @property
    def x2(self):
        return self.bbox[2]

    @property
    def y2(self):
        return self.bbox[3]

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def area(self):
        return self.width * self.height

    def to_dict(self):

        return {
            "track_id": self.track_id,
            "class_name": self.class_name,
            "confidence": round(self.confidence, 3),
            "speed": self.speed,
            "overspeed": self.overspeed,
            "wrong_way": self.wrong_way,
            "direction": self.direction,
            "has_helmet": self.has_helmet,
            "plate_text": self.plate_text,
            "bbox": self.bbox,
            "center": self.center,
        }