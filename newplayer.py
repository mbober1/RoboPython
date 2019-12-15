import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys, random, time
import threading

end_program = 0
ping = 0

                    
def Play():
    # camera = cv2.VideoCapture('http://192.168.0.206:12345/stream.mjpg')
    camera = cv2.VideoCapture('dupa.mp4')
    pygame.init()
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

    


# player_thread = threading.Thread(target = Play) 
# player_thread.start()

# while not end_program:
#     try:
#         time.sleep(1)
#         ping = random.randint(0, 5)
#         print('dupa')

#     except (KeyboardInterrupt, SystemExit):
#         end_program = 1
#         print("Exiting Main Thread")

