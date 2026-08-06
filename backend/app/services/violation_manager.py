from datetime import datetime
import json
import json
from pathlib import Path
from app.database import SessionLocal
from app.models.violation_model import Violation

class ViolationManager:
    JSON_FILE = Path("violations.json")

    def __init__(self):

        self.violations = {}
        self.active_keys = set()

    def add_violation(
        self,
        violation_type,
        track_id,
        vehicle_type,
        frame_number,
        confidence,
        metadata=None,
    ):

        key = (violation_type, track_id)

        if key in self.active_keys:
            return

        self.active_keys.add(key)

        self.violations[key] = {
            "violation_type": violation_type,
            "track_id": track_id,
            "vehicle_type": vehicle_type,
            "frame_number": frame_number,
            "confidence": confidence,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "metadata": metadata or {},
        }

    def remove_violation(
        self,
        violation_type,
        track_id,
    ):

        key = (violation_type, track_id)

        self.active_keys.discard(key)

        self.violations.pop(key, None)

    def get_all(self):

        return list(self.violations.values())

    def get_count(self):

        return len(self.violations)

    def clear(self):

        self.violations.clear()

        self.active_keys.clear()

    def add_overspeed(self, vehicle):

        if not vehicle.overspeed:
            return

        self.add_violation(
            violation_type="overspeed",
            track_id=vehicle.track_id,
            vehicle_type=vehicle.class_name,
            frame_number=vehicle.frame_number,
            confidence=1.0,
            metadata={
                "speed": vehicle.speed,
            },
        )
    def save_to_database(self):

        db = SessionLocal()

        try:

            for violation in self.violations.values():

                exists = db.query(Violation).filter(
                    Violation.track_id == violation["track_id"],
                    Violation.violation_type == violation["violation_type"],
                ).first()

                if exists:
                    continue

                db.add(

                    Violation(

                        violation_type=violation["violation_type"],

                        track_id=violation["track_id"],

                        vehicle_type=violation["vehicle_type"],

                        frame_number=violation["frame_number"],

                        confidence=violation["confidence"],

                        timestamp=violation["timestamp"],

                        violation_metadata=json.dumps(
                            violation["metadata"]
                        )
                    )

                )

            db.commit()

        finally:

            db.close()
        self.save_to_json()
    def save_to_json(self):

        data = list(self.violations.values())

        with open(
            self.JSON_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )