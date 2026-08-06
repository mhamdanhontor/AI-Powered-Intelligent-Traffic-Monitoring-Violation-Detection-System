from typing import Dict

from app.services.vehicle import Vehicle


class LineCounter:
    """
    Counts vehicles crossing a virtual horizontal line.

    A vehicle is counted only once.
    """

    def __init__(self, line_y: int = 400):

        self.line_y = line_y

        # Vehicles already counted
        self.crossed_ids = set()

        # Previous Y position of every tracked vehicle
        self.previous_y: Dict[int, int] = {}

        # Current vehicle count
        self.vehicle_count = 0

    def update(self, vehicle: Vehicle):
        """
        Update the line counter using a Vehicle object.
        """

        track_id = vehicle.track_id
        center_y = vehicle.center[1]

        previous_y = self.previous_y.get(track_id)

        # Save current position
        self.previous_y[track_id] = center_y

        # First appearance
        if previous_y is None:
            return

        # Already counted
        if track_id in self.crossed_ids:
            return

        # Vehicle crossed the line from top to bottom
        if previous_y < self.line_y <= center_y:

            self.crossed_ids.add(track_id)

            self.vehicle_count += 1

            vehicle.crossed_line = True

    def reset(self):
        """
        Reset all counters.
        """

        self.crossed_ids.clear()
        self.previous_y.clear()
        self.vehicle_count = 0