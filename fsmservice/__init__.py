import time


class FsmService:
    def __init__(self, memoryService):
        self.memoryService = memoryService
        self.min_suspicion = float(0.00)
        self.timer = 0
        self.timer_threshold = 10

    def think(self):
        has_bottles = False
        res = self.memoryService.memory.get("plasticbottles")

        if res is not None:
            has_bottles = res > self.min_suspicion
        if has_bottles and self.timer >= self.timer_threshold:
            self.timer = 0
            print("FOUND BOTTLES")

        self.timer += time.time() - getattr(self, "last_time", time.time())
        self.last_time = time.time()
        if self.timer > self.timer_threshold:
            self.timer = self.timer_threshold

        print(self.timer)
