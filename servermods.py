import RPi.GPIO as GPIO
from socket import *
import constant

class Engine:

    def __init__(self, gpio_power, gpio_dir):
        self.power = 0
        self.direction = 0
        self.gpio_power = gpio_power
        self.gpio_dir = gpio_dir
        GPIO.setup(gpio_dir, GPIO.OUT)
        GPIO.setup(gpio_power, GPIO.OUT)
        self.pwm_module = GPIO.PWM(self.gpio_power, 2500)
        self.pwm_module.start(0)
        print("Engine initialized")

    def __del__(self):
        self.pwm_module.stop()

    def set(self, new_power, new_direction):
        self.power = int(new_power*100)
        self.direction = int(new_direction)
        self.pwm_module.ChangeDutyCycle(self.power)
        GPIO.output(self.gpio_dir, self.direction)




class Server:
    def __init__(self):
        self.s = socket()
        self.s.bind((constant.HOST, constant.PORT))
        print("Server start at ", constant.HOST, constant.PORT)
        self.s.listen(1)
        self.data = ''
        self.left_trigger = 0
        self.right_trigger = 0
        self.l1 = 0
        self.r1 = 0

    def __del__(self):
        self.s.close()
        print('Connection closed')


    def wait_to_client(self):
        self.c, self.addr = self.s.accept()
        print('Got connection from', self.addr)

    def receive_data(self):
        self.data = (self.c.recv(2000)).decode()
    
    def send_data(self, data=''):
        self.c.send(data.encode())

    def handle(self):
        if self.data[0] == 'L':
            self.left_trigger = float(self.data[4:])
            print('Left Trigger: ', self.left_trigger)
            
        elif self.data[0] == 'R':
            self.right_trigger = float(self.data[4:])
            print('Right Trigger: ', self.right_trigger)

        elif self.data == 'ping':
            self.send_data('pong')

        elif self.data[0] == 'l':
            self.l1 = float(self.data[4:])
            print('L1: ', self.l1)

        elif self.data[0] == 'r':
            self.r1 = float(self.data[4:])
            print('R1: ', self.r1)
        
        elif self.data == 'close':
            print('Got shutdown command')

        else:
            print("Nieznana komenda:", self.data)
