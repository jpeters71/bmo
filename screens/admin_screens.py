from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock

from lib.battery_check import INA219
from lib.constants import MenuItems
from lib.event_queue import BmoEvent, add_event
from lib.kivy_utils import JOY_ACTION_SELECT_BUTTON_DOWN, JoystickHandler
from lib.volume import VolumeLevel, get_volume_level, set_volume_level
from lib.widgets import BmoMenu


class MainScreen(Screen, JoystickHandler):
    volume_icon = StringProperty('./media/volume/volume-high.png')
    battery_icon = StringProperty('./media/battery/battery-50.png')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._clk = None
        self._battery = INA219(addr=0x41)

    def on_enter(self):
        self.bind_joystick(self.on_joystick)
        self._update_status(None)
        self._clk = Clock.schedule_interval(self._update_status, 10)

    def on_exit(self):
        self.unbind_joystick()
        if self._clk:
            self._clk.cancel()
            self._clk = None

    def _update_status(self, dt):
        # Check the battery status
        p, charging_ind = self._battery.get_battery_percent_charging()
        if charging_ind:
            charging = 'charging-'
        else:
            charging = ''

        self.battery_icon = f'./media/battery/battery-{charging}{p}.png'

        vl = get_volume_level()
        self.volume_icon = f'./media/volume/volume-{vl.name}.png'

    def on_exit(self):
        pass

    def on_joystick(self, stick_id, action):
        if action == JOY_ACTION_SELECT_BUTTON_DOWN:
            self.main_menu()

    def main_menu(self):
        mnu = BmoMenu(
            title='Main',
            menu_items=[
                MenuItems.GAMES,
                MenuItems.VIDEOS,
                MenuItems.VOLUME,
                MenuItems.WEATHER,
                MenuItems.EXIT,
                MenuItems.EXIT_BMO,
            ],
            callback=self.menu_callback,
        )
        mnu.open()

    def menu_callback(self, cmd: str):
        if cmd == MenuItems.EXIT_BMO:
            add_event(BmoEvent('exit', {}))
        elif cmd == MenuItems.EXIT_BMO:
            add_event(BmoEvent('leave_screen', {}))
        elif cmd == MenuItems.GAMES:
            self.games_menu()
        elif cmd == MenuItems.VIDEOS:
            add_event(BmoEvent('games_menu', {}))
        elif cmd == MenuItems.WEATHER:
            add_event(BmoEvent('show_weather', {}))
        elif cmd == MenuItems.VOLUME:
            self.volume_menu()

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

    def volume_menu(self):
        self.unbind_joystick()
        mnu = BmoMenu(
            title='Volume',
            menu_items=[
                MenuItems.VOLUME_MUTE,
                MenuItems.VOLUME_LOW,
                MenuItems.VOLUME_MEDIUM,
                MenuItems.VOLUME_HIGH,
                MenuItems.EXIT,
            ],
            callback=self.volume_menu_callback,
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

    def volume_menu_callback(self, cmd: str):
        if cmd == MenuItems.VOLUME_MUTE:
            set_volume_level(VolumeLevel.mute)
        elif cmd == MenuItems.VOLUME_LOW:
            set_volume_level(VolumeLevel.low)
        elif cmd == MenuItems.VOLUME_MEDIUM:
            set_volume_level(VolumeLevel.medium)
        elif cmd == MenuItems.VOLUME_HIGH:
            set_volume_level(VolumeLevel.high)
        elif cmd == MenuItems.EXIT:
            pass
        self.bind_joystick(self.on_joystick)


class ListeningScreen(Screen):
    pass
