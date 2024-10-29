class Moment:
    def __init__(self, frame, timestamp, objects):
        self.frame = frame  # image
        self.timestamp = timestamp  # time at which the frame was captured
        self.objects = objects  # key = object, suspicion level = value


class MemoryService:
    def __init__(self, yoloService):
        self.yoloService = yoloService
        # self.last_moment = None
        self.memory = {}
        self.increment = 6
        self.confidence_threshold = 0.4
        self.decrement = 4
        self.forgetting_threshold = 0.35
        self.max = 100.0

    def remember(self, results, frame, timestamp):
        detected_objects = set()
        for result in results:
            wasa = result.boxes.cls.numpy()
            count = len(wasa)
            for obj in result.boxes.data:
                class_id = int(obj[5])
                class_name = self.yoloService.model.names[class_id]
                confidence = obj[4].item()
                detected_objects.add(class_name)

                if class_name not in self.memory:
                    self.memory[class_name] = [0.0, 0]

                self.memory[class_name][1] = count

                if confidence > self.confidence_threshold:
                    self.memory[class_name][0] = min(
                        self.max,
                        self.memory[class_name][0] + self.increment * (confidence**2),
                    )
                elif confidence < self.forgetting_threshold:
                    self.memory[class_name][0] = max(
                        0.0, self.memory[class_name][0] - self.decrement * confidence
                    )

            for class_name in list(self.memory.keys()):
                if class_name not in detected_objects:
                    self.memory[class_name][0] = max(
                        0.0, self.memory[class_name][0] - self.decrement
                    )
                    self.memory[class_name][1] = max(0, self.memory[class_name][1] - 1)

        for class_name, (level, count) in self.memory.items():
            print(f"History level for {class_name}: {level:.2f}, Count: {count}")

        # self.last_moment = Moment(frame, timestamp, self.memory)
