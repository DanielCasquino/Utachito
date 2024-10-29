import gpiod
import atexit



class LightService:
    def __init__(self):
        self.chip = gpiod.Chip("gpiochip4")
        self.led_pins = [22, 27, 17]
        self.led_lines = [self.chip.get_line(led_pin) for led_pin in self.led_pins]
        for led_line in self.led_lines:
            led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
        self.led_lines[0].set_value(1)
        self.led_lines[1].set_value(0)

    def __del__(self):
        atexit.register(self.shutdown)

    def shutdown(self):
        for led_line in self.led_lines:
            led_line.set_value(0)
            led_line.release()

    def turn_on(self, object_class):
        index = 0
        if object_class == "plasticbottles":
            index = 2
        self.led_lines[index].set_value(1)

    def turn_off(self, object_class):
        index = 0
        if object_class == "plasticbottles":
            index = 2
        self.led_lines[index].set_value(0)
