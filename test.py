import pygame, time
pygame.init()
pygame.joystick.init()
joy = pygame.joystick.Joystick(0)
joy.init()

print(joy.get_name(),' connected')


left_trigger=0
right_trigger=0

while True:
    pygame.event.get()
    rt = joy.get_axis(4)
    lt = joy.get_axis(5)
    x = joy.get_button(5)

    if x:
        print("dupa")

    if left_trigger != lt:
        left_trigger = lt
        print('LT: ',(left_trigger+1)/2)

    if right_trigger != rt:
        right_trigger = rt
        print('RT: ',(right_trigger+1)/2)