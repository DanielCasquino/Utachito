class MemoryService:
    def __init__(self, yoloService):
        self.yoloService = yoloService
        self.memory = {}
        self.increment = 6
        self.confidence_threshold = 0.6
        self.decrement = 4
        self.forgetting_threshold = 0.46
        self.max = 100.0

    def remember(self, results):
        detected_objects = set()
        for result in results:
            for obj in result.boxes.data:
                class_id = int(obj[5])
                class_name = self.yoloService.model.names[class_id]
                confidence = obj[4].item()
                detected_objects.add(class_name)

                if class_name not in self.memory:
                    self.memory[class_name] = 0.0

                if confidence > self.confidence_threshold:
                    self.memory[class_name] = min(
                        self.max,
                        self.memory[class_name] + self.increment * (confidence**2),
                    )
                elif confidence < self.forgetting_threshold:
                    self.memory[class_name] = max(
                        0.0, self.memory[class_name] - self.decrement * confidence
                    )

            for class_name in list(self.memory.keys()):
                if class_name not in detected_objects:
                    self.memory[class_name] = max(
                        0.0, self.memory[class_name] - self.decrement
                    )

        for class_name, level in self.memory.items():
            print(f"History level for {class_name}: {level:.2f}")
