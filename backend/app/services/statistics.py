class StatisticsCollector:

    def __init__(self):

        self.unique_vehicles = set()

        self.vehicle_types = {
            "car": 0,
            "truck": 0,
            "bus": 0,
            "motorcycle": 0,
        }

    def update(self, results, model):

        for box in results[0].boxes:

            if box.id is None:
                continue

            track_id = int(box.id)

            class_id = int(box.cls)

            class_name = model.names[class_id]

            if track_id not in self.unique_vehicles:

                self.unique_vehicles.add(track_id)

                if class_name in self.vehicle_types:

                    self.vehicle_types[class_name] += 1

    def get_statistics(self):

        return {

            "total_unique_vehicles": len(self.unique_vehicles),

            "vehicle_breakdown": self.vehicle_types

        }