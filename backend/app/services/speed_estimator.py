from typing import Dict

from app.services.vehicle import Vehicle


class SpeedEstimator:

    def __init__(
        self,
        line1: int = 300,
        line2: int = 500,
        distance_meters: float = 10.0,
        fps: float = 30.0,
        speed_limit: float = 60.0,
    ):

        self.line1 = line1
        self.line2 = line2

        self.distance_meters = distance_meters

        self.fps = fps

        self.speed_limit = speed_limit

        self.entry_frame: Dict[int, int] = {}

        self.vehicle_speed: Dict[int, float] = {}

        self.previous_y: Dict[int, int] = {}

    def update(self, vehicle: Vehicle):

        track_id = vehicle.track_id

        current_y = vehicle.center[1]

        previous_y = self.previous_y.get(track_id)

        self.previous_y[track_id] = current_y

        if previous_y is None:
            return

        if track_id in self.vehicle_speed:
            vehicle.speed = self.vehicle_speed[track_id]
            vehicle.overspeed = (
                vehicle.speed > self.speed_limit
            )
            return

        if (
            track_id not in self.entry_frame
            and previous_y < self.line1 <= current_y
        ):

            self.entry_frame[track_id] = vehicle.frame_number
            return

        if (
            track_id in self.entry_frame
            and previous_y < self.line2 <= current_y
        ):

            frames = (
                vehicle.frame_number
                - self.entry_frame[track_id]
            )

            if frames <= 0:
                return

            seconds = frames / self.fps

            speed = (
                self.distance_meters / seconds
            ) * 3.6

            speed = round(speed, 2)

            self.vehicle_speed[track_id] = speed

            vehicle.speed = speed

            vehicle.overspeed = (
                speed > self.speed_limit
            )

    def get_speed(self, track_id):

        return self.vehicle_speed.get(track_id)

    def reset(self):

        self.entry_frame.clear()

        self.vehicle_speed.clear()

        self.previous_y.clear()