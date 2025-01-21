from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from lib.event_queue import BmoEvent, add_event
from lib.kivy_utils import JOY_ACITON_ARROW_UP, JOY_ACTION_ARROW_DOWN, JOY_ACTION_SELECT_BUTTON_DOWN, JoystickHandler
from lib.widgets import BmoMenu
from lib.constants import MenuItems


VERT_OFFSET = 20
WINNING_SCORE = 10


class PongMenu(ScrollView):
    pass


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            Logger.info(f'VEL: {abs(bounced.x)}, {bounced.y}')
            if abs(bounced.x) < 25.0:
                Logger.info(f'Increase')
                vel = bounced * 1.25
            else:
                vel = bounced
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget, JoystickHandler):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialized = False
        self._clk = None
        self._pause = False

    def start_game(self):
        self._pause = False
        if self._clk:
            self._clk.cancel()
        self.player1.score = 0
        self.player2.score = 0
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y

        # Setup callbacks
        self.bind_joystick(self.on_joystick)

        self.serve_ball()
        self._clk = Clock.schedule_interval(self.update, 1.0 / 60.0)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        if not self._initialized:
            self.serve_ball()
            self._initialized = True
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1

            if self.player2.score >= WINNING_SCORE:
                self._end_game()
                return

            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            if self.player1.score >= WINNING_SCORE:
                self._end_game()
            self.serve_ball(vel=(-4, 0))

    def on_joystick(self, stick_id, action):
        if stick_id == 0:
            player = self.player1
        elif stick_id == 1:
            player = self.player2

        if player:
            if action == JOY_ACITON_ARROW_UP:
                if (player.top + VERT_OFFSET) < self.height:
                    player.center_y += VERT_OFFSET
            elif action == JOY_ACTION_ARROW_DOWN:
                if (player.top - VERT_OFFSET - player.height) > 0:
                    player.center_y -= VERT_OFFSET
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
            mnu =  BmoMenu(
                title='Pong',
                menu_items=[MenuItems.RESUME, MenuItems.PLAYER_VS_PLAYER, MenuItems.EXIT],
                callback=self.menu_callback)
            mnu.open()
        else:
            self.bind_joystick(self.on_joystick)
            self._clk = Clock.schedule_interval(self.update, 1.0 / 60.0)

    def main_menu(self):
        mnu =  BmoMenu(
            title='Pong',
            menu_items=[MenuItems.PLAYER_VS_PLAYER, MenuItems.EXIT],
            callback=self.menu_callback)
        mnu.open()

    def menu_callback(self, cmd: str):
        Logger.info(f'Menu item: {cmd}')

        if cmd == MenuItems.EXIT:
            add_event(BmoEvent('leave_screen', {}))
        elif cmd == MenuItems.PLAYER_VS_PLAYER:
            if self._pause:
                self._halt_game()
            self.start_game()
        elif cmd == MenuItems.RESUME:
            self._pause_resume_game()


class PongScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game = PongGame()
        self.add_widget(self._game)

    def play(self):
        self._game.main_menu()

    def on_enter(self):
        Logger.info('ENTER Pong screen')
        # self._game.play()

    def on_leave(self):
        Logger.info('LEAVE Pong screen')
        # self._game.stop()
