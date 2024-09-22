from threading import Thread
from pygame import joystick
from pygame import event
from pygame.joystick import Joystick
from kivy.logger import Logger



def init_joysticks():
    joystick.init()

    Logger.info(f'Number of joysticks: {joystick.get_count()}')
    th = Thread(target=_joystick_thread, args=[])
    th.setDaemon(True)

    th.start()
    return th


def _joystick_thread():
    js = Joystick(0)
    js.init()

    done = False
    while not done:
        for ev in event.get():
            Logger.info(f'Event {ev.type}; dict {ev.dict}')


def deinit_joysticks():
    joystick.quit()