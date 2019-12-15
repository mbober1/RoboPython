import pygame, time, threading, cv2
from clientmods import *
from pygame.locals import *

import numpy as np
import sys, random, time
import logging




def main():
    
    pygame.joystick.init()
    client = Client()
    left_trigger = 0
    right_trigger = 0
    l1_old = 0
    r1_old = 0

    try:
        joy = pygame.joystick.Joystick(0)
        joy.init()
        print(joy.get_name(), ' connected')
        try:
            client.connect()
            time1 = time.time()
            while True:
                time.sleep(0.2)
                pygame.event.get()
                rt = joy.get_axis(4)
                lt = joy.get_axis(5)
                x = joy.get_button(1)
                l1 = joy.get_button(4)
                r1 = joy.get_button(5)

                # if time.time()-time1 > 1:
                #     # client.ping()
                #     time1 = time.time()

                if left_trigger != lt:
                    left_trigger = lt
                    client.send_data('LT: ' + str(round((left_trigger + 1) / 2, 2)))

                if right_trigger != rt:
                    right_trigger = rt
                    client.send_data('RT: ' + str(round((right_trigger + 1) / 2, 2)))

                if x:
                    print('Abort!')
                    exit()

                if l1!=l1_old:
                    l1_old=l1
                    client.send_data('l1: ' + str(l1))

                if r1 != r1_old:
                    r1_old = r1
                    client.send_data('r1: ' + str(r1))

        except ConnectionRefusedError:
            print("Server refused the connection")
        except TimeoutError:
            print("Connection timeout")
        except ConnectionAbortedError:
            print("Server closed connection")

    except pygame.error as message:
        print(message)
        exit()



def Play():
    end_program = 0
    ping = 0
    # camera = cv2.VideoCapture('http://192.168.0.206:12345/stream.mjpg')
    camera = cv2.VideoCapture('dupa.mp4')
    # pygame.init()
    pygame.font.init()
    pygame.display.set_caption("RaspiRobot Camera")
    screen = pygame.display.set_mode([640,480])
    screen.fill([0,0,0])

    white = (255, 255, 255) 
    black = (0, 0, 0)
    font = pygame.font.Font('freesansbold.ttf', 11)

    while not end_program:
        try:
            ret, frame = camera.read()
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0,1)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0,0))

            text = font.render('Ping: ' + str(ping) + 'ms', True, white, black)
            screen.blit(text, (0,0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(2)
            
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            print('Preview ends')
            break

pygame.init()
threads = []
player_thread = threading.Thread(name='player', target = Play) 
threads.append(player_thread)
player_thread.setDaemon(True)
main()
# main_thread = threading.Thread(name='main', target = main) 
# ping_thread = threading.Thread(name='ping', target = client.ping) 
threads.append(main_thread)

# player_thread.start()
main_thread.start()
# ping_thread.start()

# player_thread.join()
# main_thread.join()

# while True:
#     print('dupa')
#     time.sleep(1)