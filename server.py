from socket import *
import time, constant
import RPi.GPIO as GPIO
from servermods import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(constant.GPIO_DRIVER_POWER, GPIO.OUT) #zasilanie sterownika
GPIO.output(constant.GPIO_DRIVER_POWER, GPIO.HIGH)

left_engine = Engine(constant.GPIO_LEFT_POWER,constant.GPIO_LEFT_DIR)
right_engine = Engine(constant.GPIO_RIGHT_POWER,constant.GPIO_RIGHT_DIR)

server = Server()

while True:
    server.wait_to_client()
    while not server.close:
        try:
            server.handle()
        except ValueError as message:
            print(message)

        # left_engine.set(server.left_trigger, server.l1)
        # right_engine.set(server.right_trigger, server.r1)
    
    GPIO.cleanup()
    break



