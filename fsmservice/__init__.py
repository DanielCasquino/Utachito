import random
import time


class FsmService:
    def __init__(self, memoryService):
        self.memoryService = memoryService
        self.min_suspicion = float(0.00)
        self.timer = 0
        self.timer_threshold = 10
        self.preset_messages = {
            "plasticbottles": [
                "Hola! Veo que tienes botellas de plástico. Si ya no vas a usarlas, puedes ponerlas en el tacho para plásticos.",
            ],
        }

    def think(self):
        has_bottles = False
        res = self.memoryService.memory.get("plasticbottles")

        if res is not None:
            has_bottles = res > self.min_suspicion
        if has_bottles and self.timer >= self.timer_threshold:
            self.timer = 0
            message = self.generate_message("plasticbottles")
            print(f"Generated response: {message}")

        self.timer += time.time() - getattr(self, "last_time", time.time())
        self.last_time = time.time()
        if self.timer > self.timer_threshold:
            self.timer = self.timer_threshold

        print(self.timer)

    def generate_message(self, object_class):
        messages = self.preset_messages.get(object_class, [])
        if messages:
            return random.choice(messages)
        return "No message available :("
