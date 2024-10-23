class FsmService:
    def __init__(self, memoryService):
        self.memoryService = memoryService

    def think(self):
        print("thinking...")
