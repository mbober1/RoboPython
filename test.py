import pygame, time, math
pygame.init()
pygame.joystick.init()
joy = pygame.joystick.Joystick(0)
joy.init()

print(joy.get_name(),' connected')


y_axis=0
x_axis=0
left_engine = 0
right_engine = 0
y_axis_finish = 0
x_axis_finish = 0

def Drive():
    print("L:", int(left_engine*100), "R:", int(right_engine*100))

while True:
    time.sleep(0.5)
    pygame.event.get()
    rt = joy.get_axis(0)
    lt = joy.get_axis(1)
    x = joy.get_button(5)

    # if x:
    #     print("dupa")

    if y_axis != lt:
        y_axis = lt
        y_axis_finish = -y_axis
        print('Drive: ',round(y_axis_finish,2))
        left_engine = (y_axis_finish-x_axis_finish)
        right_engine = (y_axis_finish+x_axis_finish)
        # left_engine = (math.sqrt(pow(y_axis_finish,2) + pow(x_axis_finish,2)))*(1-x_axis_finish)*y_axis_finish
        # right_engine = (math.sqrt(pow(y_axis_finish,2) + pow(x_axis_finish,2)))*(1-x_axis_finish)*y_axis_finish
        Drive()
        


    if x_axis != rt:
        x_axis = rt
        x_axis_finish = -x_axis
        print('Sterring: ',round(x_axis_finish,2))
        left_engine = (y_axis_finish-x_axis_finish)
        right_engine = (y_axis_finish+x_axis_finish)
        # left_engine = (math.sqrt(pow(y_axis_finish,2) + pow(x_axis_finish,2)))*(1-x_axis_finish)*y_axis_finish
        # right_engine = (math.sqrt(pow(y_axis_finish,2) + pow(x_axis_finish,2)))*(1-x_axis_finish)*y_axis_finish
        Drive()


    
    