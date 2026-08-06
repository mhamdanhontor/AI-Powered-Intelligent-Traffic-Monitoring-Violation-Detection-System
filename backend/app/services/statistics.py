from collections import defaultdict

from app.services.vehicle import Vehicle


class StatisticsCollector:
    """
    Collects project statistics.

    Each tracked vehicle should only be counted once.
    """

    # COCO classes we want to count
    VALID_CLASSES = {
        "car",
        "motorcycle",
        "bus",
        "truck",
    }

    def __init__(self):

        # Track IDs already counted
        self.unique_vehicle_ids = set()

        # Vehicle counts by type
        self.vehicle_counts = defaultdict(int)

        # Total detections
        self.total_unique_vehicles = 0

    def update(self, vehicle: Vehicle):
        """
        Update statistics using a Vehicle object.
        """

        if vehicle.track_id in self.unique_vehicle_ids:
            return

        self.unique_vehicle_ids.add(vehicle.track_id)

        if vehicle.class_name in self.VALID_CLASSES:

            self.vehicle_counts[vehicle.class_name] += 1

            self.total_unique_vehicles += 1

    def get_statistics(self):

        return {
            "total_unique_vehicles": self.total_unique_vehicles,
            "vehicle_breakdown": dict(self.vehicle_counts),
        }

    def reset(self):
        """
        Reset all collected statistics.
        """

        self.unique_vehicle_ids.clear()
        self.vehicle_counts.clear()
        self.total_unique_vehicles = 0