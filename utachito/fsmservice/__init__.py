import time

from utachito.chatgptservice import ChatGPTService
from utachito.ttsservice import TTSService
from utachito.awsservice import recognize


class FsmService:
    def __init__(self, memoryService):
        self.chat_gpt_service = ChatGPTService()
        self.memoryService = memoryService
        self.min_suspicion = float(0.00)
        self.timer = 0
        self.timer_threshold = 15
        self.tts_service = TTSService()

    def think(self, photo):
        """
        The photo is a numpy matrix of 3 dimensions representing a image
        """
        has_bottles = False
        res = self.memoryService.memory.get("plasticbottles")

        if res is not None:
            has_bottles = res > self.min_suspicion
        if has_bottles and self.timer >= self.timer_threshold:
            self.timer = 0
            self.generate_message(photo, "plasticbottles", 1)

        self.timer += time.time() - getattr(self, "last_time", time.time())
        self.last_time = time.time()
        if self.timer > self.timer_threshold:
            self.timer = self.timer_threshold

        print("FSM timer: ", self.timer)

    def generate_message(self, photo, object_class, amount):
        """
        The object class is the type of waste
        The amount is the number of objects
        """
        # Call to aws
        message = recognize(photo, object_class, amount)

        text = self.chat_gpt_service.get_message_for_student(message)
        self.tts_service.generate_audio([text])
        self.tts_service.play_saved_audio()
