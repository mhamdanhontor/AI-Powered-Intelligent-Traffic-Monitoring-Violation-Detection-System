from collections import defaultdict, deque
from typing import Deque, Dict, List, Tuple

from app.services.vehicle import Vehicle


class TrajectoryManager:
    """
    Stores movement history for every tracked vehicle.

    Every service (Speed, Wrong Way, Analytics, etc.)
    reads trajectory information from here.
    """

    def __init__(self, history_size: int = 30):

        self.history_size = history_size

        self.histories: Dict[int, Deque[Tuple[int, int]]] = defaultdict(
            lambda: deque(maxlen=self.history_size)
        )

    def update(self, vehicle: Vehicle):
        """
        Update trajectory history for one vehicle.
        """

        history = self.histories[vehicle.track_id]

        history.append(vehicle.center)

        vehicle.history = list(history)

    def get_history(self, track_id: int) -> List[Tuple[int, int]]:

        return list(self.histories.get(track_id, []))

    def clear(self):

        self.histories.clear()