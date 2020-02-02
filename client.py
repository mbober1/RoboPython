import pygame
import time
import cv2
from clientmods import *
from control import *
import asyncio
from ping3 import ping

stream_url = None


class Robot():
    def __init__(self):
        self.matrix = [0,0,0,0]        

    def to_matrix(self, matrix):
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
        self.matrix = matrix_out
        return matrix_out


def read_event(event):
    if event.type == pygame.KEYDOWN:

        if event.key == 97:
            y = 0
            x = -100
            # direction = 270
        
        if event.key == 100:
            y = 0
            x = 100
            # direction = 90
        
        if event.key == 119:
            # direction = 0
            x = 0
            y = 100
        
        if event.key == 115:
            x = 0
            y = -100
            # direction = 180

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
    return matrix


async def Link(stream_found_event):
    global stream_url
    
    bufor_matrix = [0,0,0,0]
    try:
        connection.connect()
        stream_url = 'Dupa'
        stream_found_event.set()
        while True:
            if bufor_matrix != car.matrix:
                bufor_matrix = car.matrix
                connection.send_data(bufor_matrix)
            
            await asyncio.sleep(0)

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
            
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP or event.type == pygame.JOYAXISMOTION:
                car.to_matrix(read_event(event))



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
    pygame.init()
    
    stream_found_event = asyncio.Event()
    await asyncio.gather(Player(stream_found_event), Link(stream_found_event))


car = Robot()
steering = Control_device()
connection = Client()

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except (KeyboardInterrupt, Exception) as e:
    print(e)
    # raise(e)
    pass
finally:
    connection.__del__()
    print('Ending program')