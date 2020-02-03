from socket import *
import constant
import RPi.GPIO as GPIO
from servermods import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(constant.GPIO_DRIVER_POWER, GPIO.OUT) #zasilanie sterownika
GPIO.output(constant.GPIO_DRIVER_POWER, GPIO.HIGH)


while True:
    server = Server()
    try:
        server.wait_to_client()
        left_engine = Engine(constant.GPIO_LEFT_POWER,constant.GPIO_LEFT_DIR)
        right_engine = Engine(constant.GPIO_RIGHT_POWER,constant.GPIO_RIGHT_DIR)
        while not server.close:
            try:
                set_engines(server.handle(), left_engine, right_engine)
            except ValueError as message:
                print(message)
        print('Connection closed')
    except KeyboardInterrupt:
        break


print('Ending program')
GPIO.cleanup()
