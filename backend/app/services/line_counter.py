from collections import defaultdict


class LineCounter:

    def __init__(self):

        self.line_y = 400

        self.crossed_ids = set()

        self.previous_positions = defaultdict(lambda: None)

        self.vehicle_count = 0

def update(self, results):

    for box in results[0].boxes:

        if box.id is None:
            continue

        track_id = int(box.id)

        x1, y1, x2, y2 = box.xyxy[0]

        center_y = int((y1 + y2) / 2)

        previous_y = self.previous_positions[track_id]

        self.previous_positions[track_id] = center_y

        if previous_y is None:
            continue

        if track_id in self.crossed_ids:
            continue

        if previous_y < self.line_y <= center_y:

            self.crossed_ids.add(track_id)

            self.vehicle_count += 1