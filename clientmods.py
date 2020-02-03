import constant
import pygame
import cv2
from socket import *
from ping3 import ping
from control import *


class Client():
    def __init__(self):
        self.connected = False
        self.s = socket()

    def __del__(self):
        if self.connected: 
                self.send_data("close")
                self.s.close()
                print("Connection closed")

        
    def connect(self):
        print('Connecting...')
        self.s.connect((constant.HOST, constant.PORT))
        print('Connected to ', constant.HOST, ':', constant.PORT)
        self.connected = True
        print('Start sending data...')
        
    def send_data(self, data=''):
        str_data = str(data)
        self.s.sendall(str_data.encode())
        print('Sent: ', str_data)

    def receive_data(self):
        return (self.s.recv(2000)).decode()



class Window():
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self):
        pygame.font.init()
        pygame.display.set_caption("Robot Camera")
        self.camera = cv2.VideoCapture(constant.LINK)
        self.screen = pygame.display.set_mode([int(self.camera.get(3)), int(self.camera.get(4))])
        self.screen.fill([0, 0, 0])
        self.font = pygame.font.Font('freesansbold.ttf', 11)
        self.displayed_frames = 0
        self.Render_ping()

    def Render_ping(self):
        temp_ping = ping(constant.HOST, unit='ms', timeout=1)
        self.ping_plane = self.font.render(
            'Ping: ' + str(int(temp_ping)) + 'ms', True, self.white, self.black)
        self.fps_plane = self.font.render(
            'Fps: ' + str(self.displayed_frames), True, self.white, self.black)
        self.displayed_frames = 0

    def Play(self):
        self.ret, self.frame = self.camera.read()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = self.frame.swapaxes(0, 1)
        self.frame = pygame.surfarray.make_surface(self.frame)
        self.screen.blit(self.frame, (0, 0))
        self.displayed_frames = self.displayed_frames+1
        
        self.screen.blit(self.ping_plane, (0, 0))
        self.screen.blit(self.fps_plane, (100, 0))



def to_matrix(matrix):
    y = matrix[1]
    x = -matrix[0]
    left_engine = (y-x)
    right_engine = (y+x)

    r_power = abs(right_engine)
    l_power = abs(left_engine)

    if r_power > 100: r_power = 100
    if l_power > 100: l_power = 100

    if left_engine < 0: l_dir = 1
    else: l_dir = 0 

    if right_engine < 0: r_dir = 1
    else: r_dir = 0 

    matrix_out = [l_power, l_dir, r_power, r_dir]
    print('Matrix out: ', matrix_out)
    return matrix_out



def read_event(event):
    if event.type == pygame.KEYDOWN:

        if event.key == 97:
            y = 0
            x = -100
        
        elif event.key == 100:
            y = 0
            x = 100
        
        elif event.key == 119:
            x = 0
            y = 100
        
        elif event.key == 115:
            x = 0
            y = -100

        elif event.key == 27:
            exit()

        else: print(event.key)

    elif event.type == pygame.KEYUP:
        x = 0
        y = 0

    else:
        global steering
        x = -int(steering.joy.get_axis(1)*100)
        y = int(steering.joy.get_axis(0)*100)

        if x > 100: x = 100
        if x < -100: x = -100
        if y > 100: y = 100
        if y < -100: y = -100

        if abs(x) < 10: x = 0
        if abs(y) < 10: y = 0

    matrix = [x, y]
    print('X: ', matrix[0], ' Y: ', matrix[1])
    return matrix

   