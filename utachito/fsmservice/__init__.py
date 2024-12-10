import time

from utachito.chatgptservice import ChatGPTService
from utachito.ttsservice import TTSService

from utachito.lightservice import LightService
from utachito.awsservice import recognize


class FsmService:
    def __init__(self, memoryService):
        self.chat_gpt_service = ChatGPTService()
        self.memoryService = memoryService
        self.min_suspicion = float(30.0)
        self.timer = 0
        self.timer_threshold = 16
        self.tts_service = TTSService()
        self.light_service = LightService()
        self.run_timer = True

    def think(self, photo, elapsed_time):
        """
        The photo is a numpy matrix of 3 dimensions representing a image
        """
        has_bottles = False
        res = self.memoryService.memory.get("plasticbottles")

        if res is not None:
            has_bottles = res[0] > self.min_suspicion
        if self.run_timer and has_bottles:
            self.timer = 0
            self.run_timer = False
            
            self.timer_threshold = elapsed_time * 50
            self.generate_message(
                photo, "plasticbottles", res[1]
            )  # res[1] is the count of plastic bottles

        self.timer += time.time() - getattr(self, "last_time", time.time())
        self.last_time = time.time()

        if self.run_timer is False and self.timer > self.timer_threshold:
            self.timer = self.timer_threshold
            self.run_timer = True

        print("FSM timer: ", self.timer)

    def generate_message(self, photo, object_class, amount):
        """
        The object class is the type of waste
        The amount is the number of objects
        """
        object_class_to_spanish = {"plasticbottles": "botella de plastico"}
        # Call to aws
        message = recognize(photo, object_class_to_spanish[object_class], amount)
        text = self.chat_gpt_service.get_message_for_student(message)
        self.tts_service.generate_audio([text])
        self.light_service.turn_on(object_class)
        self.tts_service.play_saved_audio()
        self.light_service.turn_off(object_class)
        # self.run_timer = True
        # solo corre una vez por ahora si no lo ponemos en true
