import time

from utachito.chatgptservice import ChatGPTService
from utachito.ttsservice import TTSService

class FsmService:
    def __init__(self, memoryService):
        self.chat_gpt_service = ChatGPTService()
        self.memoryService = memoryService
        self.min_suspicion = float(0.00)
        self.timer = 0
        self.timer_threshold = 10
        self.tts_service = TTSService()

    def think(self):
        has_bottles = False
        res = self.memoryService.memory.get("plasticbottles")

        if res is not None:
            has_bottles = res > self.min_suspicion
        if has_bottles and self.timer >= self.timer_threshold:
            self.timer = 0
            self.generate_message("plasticbottles")

        self.timer += time.time() - getattr(self, "last_time", time.time())
        self.last_time = time.time()
        if self.timer > self.timer_threshold:
            self.timer = self.timer_threshold

        print(self.timer)

    def generate_message(self, object_class):
        text = self.chat_gpt_service.get_message_for_student(object_class)
        self.tts_service.generate_audio([text])
        self.tts_service.play_saved_audio()
        
