class StatisticsCollector:

    def __init__(self):
        self.stats = {
            "car": 0,
            "truck": 0,
            "bus": 0,
            "motorcycle": 0
        }

    def update(self, results, model):

        for box in results[0].boxes:

            class_id = int(box.cls)
            class_name = model.names[class_id]

            if class_name in self.stats:
                self.stats[class_name] += 1

    def get_statistics(self):
        return self.stats