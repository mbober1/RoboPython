import pygame, time, threading, cv2
from clientmods import *
import asyncio
from pygame.locals import *
from ping3 import ping

import numpy as np
import sys, random, time
import logging


def FindJoysticks():
    print("Found " + str(pygame.joystick.get_count()) + " devices")
    if pygame.joystick.get_count()>1: 
        for i in range(0, pygame.joystick.get_count()):
            print('[' + str(i) + ']' + pygame.joystick.Joystick(i).get_name())
        device = int(input("Choose one: "))
    else: device = 0

    return device

class Control_device():
    axis_data = None
    button_data = None
    power = None
    direction = None
    
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if(pygame.joystick.get_count()):
            try:
                self.keyboard = 0
                self.joy = pygame.joystick.Joystick(FindJoysticks())
                self.joy.init()
                print(self.joy.get_name(), ' connected')
                print(self.joy.get_numaxes(), 'Axes,', self.joy.get_numbuttons(), 'Buttons')

            except pygame.error as message:
                self.keyboard = 1
                print("Keyboard control")

        else: 
            self.keyboard = 1
            print("Keyboard control")

    
    def listen(self):
        if not self.axis_data:
            self.axis_data = {}
            
        for event in pygame.event.get():
            print('E:', event)
            if event.type == pygame.key.get_pressed():
                print("wcisniety")
                if event.key == pygame.K_LEFT:
                    print("lewo")
                    self.power = 100
                    self.direction = 270

                if event.key == pygame.K_RIGHT:
                    print("prawo")
                    self.power = 100
                    self.direction = 90

            elif event.type == pygame.JOYAXISMOTION:
                # print('pad')
                self.axis_data[event.axis] = round(event.value,2)

        # if not self.keyboard:
        
        #     if not self.axis_data:
        #         self.axis_data = {}

        #     # if not self.button_data:
        #     #     self.button_data = {}
        #     #     for i in range(self.joy.get_numbuttons()):
        #     #         self.button_data[i] = False


        #     # print(f'C:{pygame.e}')
        #     for event in pygame.event.get():
        #         if event.type == pygame.JOYAXISMOTION:
        #             self.axis_data[event.axis] = round(event.value,2)
        #         # elif event.type == pygame.JOYBUTTONDOWN:
        #         #     self.button_data[event.button] = True
        #         # elif event.type == pygame.JOYBUTTONUP:
        #         #     self.button_data[event.button] = False

        #             # Insert your code on what you would like to happen for each event here!
        #             # In the current setup, I have the state simply printing out to the screen.
        #         print(9)
        #         return self.axis_data
        
        # if self.keyboard: #TU SKONCZYLEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111111  
        #     print("dupa1")
        #     for event in pygame.event.get():
        #         print("dupa")
        #         if event.type == pygame.key.get_pressed():
        #             print("wcisniety")
        #             if event.key == pygame.K_LEFT:
        #                 print("lewo")
        #                 self.power = 100
        #                 self.direction = 270

        #             if event.key == pygame.K_RIGHT:
        #                 print("prawo")
        #                 self.power = 100
        #                 self.direction = 90



async def Control():
    connection = Client()
    steering = Control_device()
    try:
        # connection.connect()
        time1 = time.time()
        while True:
            try:
                # time.sleep(0.2)
                await asyncio.sleep(0)
                # print(steering.listen())
                # pygame.event.get()

                # rt = joy.get_axis(4)
                # lt = joy.get_axis(5)
                # x = joy.get_button(1)
                # l1 = joy.get_button(4)
                # r1 = joy.get_button(5)

                # if left_trigger != lt:
                #     left_trigger = lt
                #     connection.send_data('LT: ' + str(round((left_trigger + 1) / 2, 2)))

                # if right_trigger != rt:
                #     right_trigger = rt
                #     connection.send_data('RT: ' + str(round((right_trigger + 1) / 2, 2)))

                # if x:
                #     print('Abort!')
                #     exit()

                # if l1!=l1_old:
                #     l1_old=l1
                #     connection.send_data('l1: ' + str(l1))

                # if r1 != r1_old:
                #     r1_old = r1
                #     connection.send_data('r1: ' + str(r1))
            except KeyboardInterrupt:
                print('Control ends')
                break

    except ConnectionRefusedError:
        print("Server refused the connection")
    except TimeoutError:
        print("Connection timeout")
    except ConnectionAbortedError:
        print("Server closed connection")


        








async def Player():
    
    window = Window()

    timer = time.time()
    while True:
        await asyncio.sleep(0)
        try:
            fps_timer = time.time()
            if(time.time()- timer > 1):
                window.Render_ping()
                timer = time.time()

            window.Play()
            pygame.display.update()

            if (time.time()-fps_timer) < (1/constant.FPS):
                time.sleep((1/constant.FPS)-(time.time()-fps_timer))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(2)
            
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            print('Preview ends')
            break


class Window():
    white = (255, 255, 255) 
    black = (0, 0, 0)

    def __init__(self):
        pygame.font.init()
        pygame.display.set_caption("RaspiRobot Camera")
        self.screen = pygame.display.set_mode([640,480])
        self.screen.fill([0,0,0])
        self.font = pygame.font.Font('freesansbold.ttf', 11)
        self.fps = 0
        self.Render_ping()
        self.camera = cv2.VideoCapture(constant.LINK)
    
    def Render_ping(self):
        temp_ping = ping(constant.HOST, unit='ms', timeout=1)
        self.ping_plane = self.font.render('Ping: ' + str(int(temp_ping)) + 'ms', True, self.white, self.black)
        self.fps_plane = self.font.render('Fps: ' + str(self.fps), True, self.white, self.black)
        self.fps=0

    def Play(self):
        self.ret, self.frame = self.camera.read()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = self.frame.swapaxes(0,1)
        self.frame = pygame.surfarray.make_surface(self.frame)
        self.screen.blit(self.frame, (0,0))
        self.fps = self.fps+1

        self.screen.blit(self.ping_plane, (0,0))
        self.screen.blit(self.fps_plane, (100,0))
        

async def main():
    try:
        pygame.init()
        ft = asyncio.gather(Player(), Control())
        await asyncio.sleep(5)
        ft.cancel()
    except asyncio.exceptions.CancelledError:
        print('dupaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

asyncio.run(main())