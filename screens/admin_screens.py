from kivy.uix.screenmanager import Screen

from lib.constants import MenuItems
from lib.event_queue import BmoEvent, add_event
from lib.kivy_utils import JOY_ACTION_SELECT_BUTTON_DOWN, JoystickHandler
from lib.widgets import BmoMenu


class MainScreen(Screen, JoystickHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.bind_joystick(self.on_joystick)

    def on_joystick(self, stick_id, action):
        if action == JOY_ACTION_SELECT_BUTTON_DOWN:
            self.main_menu()

    def main_menu(self):
        mnu = BmoMenu(title='Main', menu_items=[MenuItems.GAMES, MenuItems.VIDEOS, MenuItems.EXIT], callback=self.menu_callback)
        mnu.open()

    def menu_callback(self, cmd: str):
        if cmd == MenuItems.EXIT:
            add_event(BmoEvent('exit', {}))
        elif cmd == MenuItems.GAMES:
            self.games_menu()
        elif cmd == MenuItems.VIDEOS:
            add_event(BmoEvent('games_menu', {}))

    def games_menu(self):
        self.unbind_joystick()
        mnu = BmoMenu(
            title='Games',
            menu_items=[
                MenuItems.LIGHTCYCLES,
                MenuItems.PONG,
                MenuItems.SNAKE,
                MenuItems.TETRIS,
                MenuItems.EXIT,
            ],
            callback=self.games_menu_callback,
        )
        mnu.open()

    def games_menu_callback(self, cmd: str):
        if cmd == MenuItems.LIGHTCYCLES:
            add_event(BmoEvent('play_game', {'game': 'lightcycles'}))
        elif cmd == MenuItems.PONG:
            add_event(BmoEvent('play_game', {'game': 'pong'}))
        elif cmd == MenuItems.SNAKE:
            add_event(BmoEvent('play_game', {'game': 'snake'}))
        elif cmd == MenuItems.TETRIS:
            add_event(BmoEvent('play_game', {'game': 'tetris'}))
        elif cmd == MenuItems.EXIT:
            pass


class ListeningScreen(Screen):
    pass
