from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from lib.constants import CTRL_AXIS_VERTICAL, CTRL_UP_ARROW, CTRL_DOWN_ARROW


VERT_OFFSET = 20


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


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialized = False

        # Setup callbacks
        Window.bind(on_joy_hat=self.on_joy_hat)
        Window.bind(on_joy_ball=self.on_joy_ball)
        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_up=self.on_joy_button_up)
        Window.bind(on_joy_button_down=self.on_joy_button_down)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

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
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))


    def on_joy_axis(self, win, stick_id, axis_id, value):
        if axis_id == 1:
            if stick_id == 0:
                player = self.player1
            elif stick_id == 1:
                player = self.player2

            if player:
                if value == CTRL_UP_ARROW:
                    if (player.top + VERT_OFFSET) < self.height:
                        player.center_y += VERT_OFFSET
                elif value == CTRL_DOWN_ARROW:
                    if (player.top - VERT_OFFSET - player.height) > 0:
                        player.center_y -= VERT_OFFSET

        Logger.info(f'Axis [{stick_id}]: [{axis_id}]: {value}')

    def on_joy_ball(self, win, stickid, ballid, xvalue, yvalue):
        Logger.info(f'Ball [{stickid}]: [{ballid}]: {xvalue}, {yvalue}')

    def on_joy_hat(self, win, stickid, hatid, value):
        Logger.info(f'Hat [{stickid}]: [{hatid}]: {value}')

    def on_joy_button_down(self, win, stickid, buttonid):
        Logger.info(f'Button down [{stickid}]: {buttonid}')

    def on_joy_button_up(self, win, stickid, buttonid):
        Logger.info(f'Button up [{stickid}]: {buttonid}')
