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