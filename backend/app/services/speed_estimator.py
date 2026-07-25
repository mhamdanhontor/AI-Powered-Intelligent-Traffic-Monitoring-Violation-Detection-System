import time


class SpeedEstimator:

    def __init__(self):

        self.line1 = 300
        self.line2 = 500

        self.distance_meters = 10

        self.entry_time = {}

        self.exit_time = {}

        self.vehicle_speed = {}

    def update(self, results):

        for box in results[0].boxes:

            if box.id is None:
                continue

            track_id = int(box.id)

            x1, y1, x2, y2 = box.xyxy[0]

            center_y = int((y1 + y2) / 2)

            current_time = time.time()

            if track_id not in self.entry_time:

                if center_y >= self.line1:

                    
                    self.entry_time[track_id] = current_time

            if track_id in self.entry_time:

                if track_id not in self.vehicle_speed:

                    if center_y >= self.line2:

                        elapsed = current_time - self.entry_time[track_id]

                        if elapsed > 0:

                            speed = (self.distance_meters / elapsed) * 3.6

                            self.vehicle_speed[track_id] = round(speed, 2)