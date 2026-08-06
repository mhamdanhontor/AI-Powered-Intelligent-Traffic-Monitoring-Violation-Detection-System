from collections import defaultdict


class WrongWayDetector:
    """
    Detect vehicles travelling opposite to the allowed direction.

    Allowed directions:
        down  -> increasing y
        up    -> decreasing y
        left  -> decreasing x
        right -> increasing x
    """

    def __init__(
        self,
        violation_manager,
        allowed_direction="down",
        minimum_distance=40,
    ):

        self.violation_manager = violation_manager

        self.allowed_direction = allowed_direction.lower()

        self.minimum_distance = minimum_distance

        self.violating_ids = set()

    def update(self, vehicle):

        history = vehicle.history

        if history is None:
            return

        if len(history) < 8:
            return

        start_x, start_y = history[0]
        end_x, end_y = history[-1]

        dx = end_x - start_x
        dy = end_y - start_y

        if abs(dx) > abs(dy):

            if abs(dx) < self.minimum_distance:
                return

            direction = "right" if dx > 0 else "left"

            score = abs(dx)

        else:

            if abs(dy) < self.minimum_distance:
                return

            direction = "down" if dy > 0 else "up"

            score = abs(dy)

        vehicle.direction = direction
        vehicle.direction_score = score

        if direction != self.allowed_direction:

            vehicle.wrong_way = True

            if vehicle.track_id not in self.violating_ids:

                self.violating_ids.add(vehicle.track_id)

                self.violation_manager.add_violation(
                    violation_type="wrong_way",
                    track_id=vehicle.track_id,
                    vehicle_type=vehicle.class_name,
                    frame_number=vehicle.frame_number,
                    confidence=vehicle.confidence,
                    metadata={
                        "direction": direction,
                        "allowed_direction": self.allowed_direction,
                    },
                )

        else:

            vehicle.wrong_way = False

            if vehicle.track_id in self.violating_ids:

                self.violating_ids.remove(vehicle.track_id)

                self.violation_manager.remove_violation(
                    "wrong_way",
                    vehicle.track_id,
                )