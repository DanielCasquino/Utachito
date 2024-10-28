import gpiod
import atexit


class LightService:
    def __init__(self):
        self.chip = gpiod.Chip("gpiochip4")
        self.led_pins = [22, 27, 17]
        self.led_lines = [chip.get_line(led_pin) for led_pin in led_pins]
        # No se para que sirve lo de abajo
        for led_line in led_lines:
            led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

        # Prender 22 al principio. O sea que sea 1
        led_lines[1].set_value(1)
        # Apagar 27 al principio. O sea que sea 0
        led_lines[2].set_value(0)

    def __del__(self):
        atexit.register(shutdown)

    def shutdown():
        for led_line in led_lines:
            led_line.set_value(0)
            led_line.release()

    def turn_on(object_class):
        index = 0
        if object_class == "plasticbottles":
            index = 2
        led_lines[index].set_value(1)

    def turn_off(object_class):
        index = 0
        if object_class == "plasticbottles":
            index = 2
        led_lines[index].set_value(0)
