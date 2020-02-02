import pygame
import time
import cv2
from clientmods import *
from control import *
import asyncio
from ping3 import ping


stream_url = None

class Engine:
    def __init__(self):
        self.power = 0
        self.reverse = 0
    
    def set(self, power, reverse):
        self.power = power
        self.reverse = reverse



def keyboard_sterring(event):    
    if event.type == pygame.KEYDOWN:
        power = 100

        if event.key == 97:
            direction = 270
        
        if event.key == 100:
            direction = 90
        
        if event.key == 119:
            direction = 0
        
        if event.key == 115:
            direction = 180


    elif event.type == pygame.KEYUP:
        power = 0

        if event.key == 97:
            direction = 270
        
        if event.key == 100:
            direction = 90
        
        if event.key == 119:
            direction = 0
        
        if event.key == 115:
            direction = 180
    
    matrix = [power, direction]
    return matrix

def joystick_sterring(event):
    print(event) #TODOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO


async def Link(stream_found_event):
    global stream_url
    connection = Client()
    steering = Control_device()
    try:
        # connection.connect()
        stream_url = 'Dupa'
        stream_found_event.set()
        while True:
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

    except ConnectionRefusedError:
        print("Server refused the connection")
    except TimeoutError:
        print("Connection timeout")
    except ConnectionAbortedError:
        print("Server closed connection")


async def Player(stream_found_event):
    global stream_url
    await stream_found_event.wait()
    window = Window()

    timer = time.time()
    fps_set = window.camera.get(5)
    while True:
        await asyncio.sleep(0)
        fps_timer = time.time()
        if(time.time() - timer > 1):
            window.Render_ping()
            timer = time.time()

        window.Play()
        pygame.display.update()

        if (time.time()-fps_timer) < (1/fps_set):
            time.sleep((1/fps_set)-(time.time()-fps_timer))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception()
            
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                print(keyboard_sterring(event))
            
            elif event.type == pygame.JOYAXISMOTION:
                print(joystick_sterring(event))



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






async def main():
    left_engine = Engine()
    right_engine = Engine()
    pygame.init()
    stream_found_event = asyncio.Event()
    await asyncio.gather(Player(stream_found_event), Link(stream_found_event))


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except (KeyboardInterrupt, Exception) as e:
    print(e)
    pass
finally:
    print('Ending program')