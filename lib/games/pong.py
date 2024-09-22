from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from random import randint


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Setup callbacks
        Window.bind(on_joy_hat=self.on_joy_hat)
        Window.bind(on_joy_ball=self.on_joy_ball)
        Window.bind(on_joy_axis=self.on_joy_axis)
        Window.bind(on_joy_button_up=self.on_joy_button_up)
        Window.bind(on_joy_button_down=self.on_joy_button_down)



    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1


    def on_joy_axis(self, win, stickid, axisid, value):
        Logger.info(f'Axis [{stickid}]: [{axisid}]: {value}')

    def on_joy_ball(self, win, stickid, ballid, xvalue, yvalue):
        Logger.info(f'Ball [{stickid}]: [{ballid}]: {xvalue}, {yvalue}')

    def on_joy_hat(self, win, stickid, hatid, value):
        Logger.info(f'Hat [{stickid}]: [{hatid}]: {value}')

    def on_joy_button_down(self, win, stickid, buttonid):
        Logger.info(f'Button down [{stickid}]: {buttonid}')

    def on_joy_button_up(self, win, stickid, buttonid):
        Logger.info(f'Button up [{stickid}]: {buttonid}')