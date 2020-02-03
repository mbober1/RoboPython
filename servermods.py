import RPi.GPIO as GPIO
from socket import *
import constant
import ast

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

    def set_engine(self, new_power, new_direction):
        self.power = new_power
        self.direction = new_direction
        self.pwm_module.ChangeDutyCycle(self.power)
        GPIO.output(self.gpio_dir, self.direction)


def set_engines(matrix, e1, e2):
    print(matrix)
    e1.set_engine(matrix[0], matrix[1])
    e2.set_engine(matrix[2], matrix[3])

class Server:
    def __init__(self):
        self.close = False
        self.s = socket()
        self.s.bind((constant.HOST, constant.PORT))
        print("Server start at ", constant.HOST, constant.PORT)
        self.s.listen(1)

    def __del__(self):
        self.s.close()
        print('Connection closed')

    def wait_to_client(self):
        self.c, self.addr = self.s.accept()
        print('Got connection from', self.addr)

    def receive_data(self):
        data = (self.c.recv(2000)).decode()
        return data
    
    def send_data(self, data=''):
        self.c.send(data.encode())

    def handle(self):
        data = self.receive_data()
        print('Recived: ', data)
        if data[0] == '[':
            bufor = ast.literal_eval(data)
            print('Transformated to: ', bufor)
            return bufor
        
        elif data == 'close':
            print('Got shutdown command')
            self.close = True
            return [0,0,0,0]

        else:
            print("Unkown command:", data)
