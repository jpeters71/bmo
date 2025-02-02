from random import randint

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.vector import Vector
from lib.constants import MenuItems
from lib.event_queue import BmoEvent, add_event
from lib.games import SmartGrid
from lib.kivy_utils import (
    JOY_ACITON_ARROW_UP,
    JOY_ACTION_ARROW_DOWN,
    JOY_ACTION_ARROW_LEFT,
    JOY_ACTION_ARROW_RIGHT,
    JOY_ACTION_SELECT_BUTTON_DOWN,
    JoystickHandler,
)
from lib.widgets import BmoMenu

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 800

# note that 2 pixels are always subtracted from PLAYER_SIZE for better clarity
PLAYER_SIZE = 40
GAME_SPEED = 0.1


class SnakeFruit(Widget):
    def move(self, new_pos):
        self.pos = new_pos


class SnakeTail(Widget):
    def move(self, new_pos):
        self.pos = new_pos


class SnakeHead(Widget):
    orientation = (PLAYER_SIZE, 0)

    def reset_pos(self):
        # positions the player roughly in the middle of the gameboard
        self.pos = [
            int(WINDOW_WIDTH / 2 - (WINDOW_WIDTH / 2 % PLAYER_SIZE)),
            int(WINDOW_HEIGHT / 2 - (WINDOW_HEIGHT / 2 % PLAYER_SIZE)),
        ]
        self.orientation = (PLAYER_SIZE, 0)

    def move(self):
        self.pos = Vector(*self.orientation) + self.pos


class SnakeGame(Widget, JoystickHandler):

    head = ObjectProperty(None)
    fruit = ObjectProperty(None)
    score = NumericProperty(0)
    player_size = NumericProperty(PLAYER_SIZE)
    game_over = StringProperty("")

    def __init__(self):
        super(SnakeGame, self).__init__()

        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        Window.bind(on_key_down=self.key_action)

        if PLAYER_SIZE < 3:
            raise ValueError("Player size should be at least 3 px")

        if WINDOW_HEIGHT < 3 * PLAYER_SIZE or WINDOW_WIDTH < 3 * PLAYER_SIZE:
            raise ValueError("Window size must be at least 3 times larger than player size")
        self._clk = None
        self._pause = False
        self.tail = []

    def start_game(self):
        self._pause = False

        # Setup callbacks
        self.bind_joystick(self.on_joystick)
        self.occupied = SmartGrid(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

        self.head.reset_pos()
        self.score = 0

        for block in self.tail or []:
            self.remove_widget(block)

        # the tail is indexed in a way that the last block is idx 0
        for t in self.tail:
            self.remove_widget(t)
        self.tail = []

        # first two blocks added to the tail
        self.tail.append(SnakeTail(pos=(self.head.pos[0] - PLAYER_SIZE, self.head.pos[1]), size=(self.head.size)))
        self.add_widget(self.tail[-1])
        self.occupied[self.tail[-1].pos] = True

        self.tail.append(SnakeTail(pos=(self.head.pos[0] - 2 * PLAYER_SIZE, self.head.pos[1]), size=(self.head.size)))
        self.add_widget(self.tail[-1])
        self.occupied[self.tail[1].pos] = True

        self.spawn_fruit()

        # resets the timer
        if self._clk:
            self._clk.cancel()
        self._clk = Clock.schedule_interval(self.refresh, GAME_SPEED)

    def refresh(self, dt):
        """This block of code is executed every GAME_SPEED seconds

        'dt' must be used to allow kivy.Clock objects to use this function
        """

        # outside the boundaries of the game
        if not (0 <= self.head.pos[0] < WINDOW_WIDTH) or not (0 <= self.head.pos[1] < WINDOW_HEIGHT):
            self._end_game()
            return

        # collides with its tail
        if self.occupied[self.head.pos] is True:
            self._end_game()
            return

        # move the tail
        self.occupied[self.tail[-1].pos] = False
        self.tail[-1].move(self.tail[-2].pos)

        for i in range(2, len(self.tail)):
            self.tail[-i].move(new_pos=(self.tail[-(i + 1)].pos))

        self.tail[0].move(new_pos=self.head.pos)
        self.occupied[self.tail[0].pos] = True

        # move the head
        self.head.move()

        # check if we found the fruit, if so, add another tail
        if self.head.pos == self.fruit.pos:
            self.score += 1
            self.tail.append(SnakeTail(pos=self.head.pos, size=self.head.size))
            self.add_widget(self.tail[-1])
            self.spawn_fruit()

    def spawn_fruit(self):
        roll = self.fruit.pos
        found = False
        while not found:

            # roll new random positions until one is free
            roll = [
                PLAYER_SIZE * randint(0, int(WINDOW_WIDTH / PLAYER_SIZE) - 1),
                PLAYER_SIZE * randint(0, int(WINDOW_HEIGHT / PLAYER_SIZE) - 1),
            ]

            if self.occupied[roll] is True or roll == self.head.pos:
                continue

            found = True

        self.fruit.move(roll)

    def key_action(self, *args):
        """This handles user input"""
        command = list(args)[3]

        if command == 'w' or command == 'up':
            self.head.orientation = (0, PLAYER_SIZE)
        elif command == 's' or command == 'down':
            self.head.orientation = (0, -PLAYER_SIZE)
        elif command == 'a' or command == 'left':
            self.head.orientation = (-PLAYER_SIZE, 0)
        elif command == 'd' or command == 'right':
            self.head.orientation = (PLAYER_SIZE, 0)
        elif command == 'r':
            self.restart_game()

    def on_joystick(self, stick_id, action):
        if action == JOY_ACITON_ARROW_UP:
            self.head.orientation = (0, PLAYER_SIZE)
        elif action == JOY_ACTION_ARROW_DOWN:
            self.head.orientation = (0, -PLAYER_SIZE)
        elif action == JOY_ACTION_ARROW_LEFT:
            self.head.orientation = (-PLAYER_SIZE, 0)
        elif action == JOY_ACTION_ARROW_RIGHT:
            self.head.orientation = (PLAYER_SIZE, 0)
        elif action == JOY_ACTION_SELECT_BUTTON_DOWN:
            self._pause_resume_game()

    def _end_game(self):
        Logger.info('Game over')
        self._halt_game()
        self.main_menu()

    def _halt_game(self):
        if self._clk:
            self._clk.cancel()
            self._clk = None
        self.unbind_joystick()

    def _pause_resume_game(self):
        if self._clk:
            self._clk.cancel()
            self._clk = None
            self._pause = True
            self.unbind_joystick()
            mnu = BmoMenu(
                title='Snake',
                menu_items=[MenuItems.RESUME, MenuItems.PLAYER_VS_COMPUTER, MenuItems.EXIT],
                callback=self.menu_callback,
            )
            mnu.open()
        else:
            self.bind_joystick(self.on_joystick)
            self._clk = Clock.schedule_interval(self.update, 1.0 / 60.0)

    def main_menu(self):
        mnu = BmoMenu(title='Snake', menu_items=[MenuItems.PLAYER_VS_COMPUTER, MenuItems.EXIT], callback=self.menu_callback)
        mnu.open()

    def menu_callback(self, cmd: str):
        Logger.info(f'Menu item: {cmd}')

        if cmd == MenuItems.EXIT:
            add_event(BmoEvent('leave_screen', {'type': 'game'}))
        elif cmd == MenuItems.PLAYER_VS_COMPUTER:
            if self._pause:
                self._halt_game()
            self.start_game()
        elif cmd == MenuItems.RESUME:
            self._pause_resume_game()


class SnakeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game = SnakeGame()
        self.add_widget(self._game)

    def play(self):
        self._game.main_menu()

    def on_enter(self):
        Logger.info('ENTER Snake screen')
        self._game.main_menu()

    def on_leave(self):
        Logger.info('LEAVE Snake screen')
        # self._game.stop()
