from kivy.core.window import Window

from typing import Callable

from lib.constants import CTLR_BUTTON_A, CTLR_BUTTON_B, CTLR_BUTTON_SELECT, CTLR_BUTTON_START, CTRL_AXIS_HORIZONTAL, CTRL_AXIS_VERTICAL, CTRL_DOWN_ARROW, CTRL_LEFT_ARROW, CTRL_RELEASE_ARROW, CTRL_RIGHT_ARROW, CTRL_UP_ARROW


JOY_ACTION_A_BUTTON_DOWN = 1
JOY_ACTION_A_BUTTON_UP = 2
JOY_ACTION_B_BUTTON_DOWN = 3
JOY_ACTION_B_BUTTON_UP = 4
JOY_ACTION_START_BUTTON_DOWN = 5
JOY_ACTION_START_BUTTON_UP = 6
JOY_ACTION_SELECT_BUTTON_DOWN = 7
JOY_ACTION_SELECT_BUTTON_UP = 8
JOY_ACITON_ARROW_UP = 9
JOY_ACTION_ARROW_DOWN = 10
JOY_ACTION_ARROW_LEFT = 11
JOY_ACTION_ARROW_RIGHT = 12
JOY_ACITON_RELEASE_ARROW = 13


class JoystickHandler:
    def __init__(self):
        self._callback = None

    def bind_joystick(self, callback: Callable[[int, int], int]):
        self._callback: Callable[[int, int], int] = callback
        Window.bind(on_joy_hat=self._on_joy_hat)
        Window.bind(on_joy_ball=self._on_joy_ball)
        Window.bind(on_joy_axis=self._on_joy_axis)
        Window.bind(on_joy_button_up=self._on_joy_button_up)
        Window.bind(on_joy_button_down=self._on_joy_button_down)

    def unbind_joystick(self):
        if self._callback:
            Window.unbind(on_joy_hat=self._on_joy_hat)
            Window.unbind(on_joy_ball=self._on_joy_ball)
            Window.unbind(on_joy_axis=self._on_joy_axis)
            Window.unbind(on_joy_button_up=self._on_joy_button_up)
            Window.unbind(on_joy_button_down=self._on_joy_button_down)
            self._callback = None

    def _on_joy_axis(self, win, stick_id, axis_id, value):
        if axis_id == CTRL_AXIS_VERTICAL:
            if value == CTRL_UP_ARROW:
                self._callback(stick_id, JOY_ACITON_ARROW_UP)
            elif value == CTRL_DOWN_ARROW:
                self._callback(stick_id, JOY_ACTION_ARROW_DOWN)
            elif value == CTRL_RELEASE_ARROW:
                self._callback(stick_id, JOY_ACITON_RELEASE_ARROW)
        elif axis_id == CTRL_AXIS_HORIZONTAL:
            if value == CTRL_LEFT_ARROW:
                self._callback(stick_id, JOY_ACTION_ARROW_LEFT)
            elif value == CTRL_RIGHT_ARROW:
                self._callback(stick_id, JOY_ACTION_ARROW_RIGHT)
            elif value == CTRL_RELEASE_ARROW:
                self._callback(stick_id, JOY_ACITON_RELEASE_ARROW)

    def _on_joy_ball(self, win, stickid, ballid, xvalue, yvalue):
        # We don't currently need this.
        pass

    def _on_joy_hat(self, win, stickid, hatid, value):
        # We don't currently need this.
        pass

    def _on_joy_button_down(self, win, stickid, buttonid):
        if buttonid == CTLR_BUTTON_A:
            self._callback(stickid, JOY_ACTION_A_BUTTON_DOWN)
        elif buttonid == CTLR_BUTTON_B:
            self._callback(stickid, JOY_ACTION_B_BUTTON_DOWN)
        elif buttonid == CTLR_BUTTON_START:
            self._callback(stickid, JOY_ACTION_START_BUTTON_DOWN)
        elif buttonid == CTLR_BUTTON_SELECT:
            self._callback(stickid, JOY_ACTION_SELECT_BUTTON_DOWN)

    def _on_joy_button_up(self, win, stickid, buttonid):
        if buttonid == CTLR_BUTTON_A:
            self._callback(stickid, JOY_ACTION_A_BUTTON_UP)
        elif buttonid == CTLR_BUTTON_B:
            self._callback(stickid, JOY_ACTION_B_BUTTON_UP)
        elif buttonid == CTLR_BUTTON_START:
            self._callback(stickid, JOY_ACTION_START_BUTTON_UP)
        elif buttonid == CTLR_BUTTON_SELECT:
            self._callback(stickid, JOY_ACTION_SELECT_BUTTON_UP)

