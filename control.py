import pygame


def FindJoysticks():
    print("Found " + str(pygame.joystick.get_count()) + " devices")
    if pygame.joystick.get_count() > 1:
        for i in range(0, pygame.joystick.get_count()):
            print('[' + str(i) + ']' + pygame.joystick.Joystick(i).get_name())
        device = int(input("Choose one: "))
    else:
        device = 0

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
                print(self.joy.get_numaxes(), 'Axes,',
                      self.joy.get_numbuttons(), 'Buttons')

            except pygame.error as message:
                self.keyboard = 1
                print("Keyboard control")

        else:
            self.keyboard = 1
            print("Keyboard control")

    # def listen(self):
    #     if not self.axis_data:
    #         self.axis_data = {}

    #     for event in pygame.event.get():
    #         print('E:', event)
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

    #         elif event.type == pygame.JOYAXISMOTION:
    #             # print('pad')
    #             self.axis_data[event.axis] = round(event.value, 2)

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
