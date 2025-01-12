from gc import callbacks
from typing import Callable
from kivy.uix.button import Button
from kivy.uix.behaviors import FocusBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.properties import BooleanProperty

from kivy.core.window import Window

from lib.constants import KEY_DOWN, KEY_ENTER, KEY_TAB, KEY_UP
from lib.kivy_utils import JOY_ACITON_ARROW_UP, JOY_ACTION_A_BUTTON_DOWN, JOY_ACTION_ARROW_DOWN, JOY_ACTION_SELECT_BUTTON_DOWN, JoystickHandler

class FocusButton(Button):
    current_focus = BooleanProperty()
    pass
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(current_focus=self.on_current_focus)

    def on_current_focus(self, instance, value):
        Logger.info(f'Button: {instance.text}, Focus: {value}')
        if value:
            self.background_color = (0, 0, 1, 1)
        else:
            self.background_color = (1, 1, 0, 0)


class BmoMenuOptions(BoxLayout):
    def __init__(self, form_fields: list[str],  **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.options = []
        for field in form_fields:
            opt = FocusButton(text=field)
            self.add_widget(opt)
            self.options.append(opt)

    def on_key_down(self, window, key, *args):
        if key == KEY_TAB:
            if len(args) > 2:
                if 'shift' in args[2]:
                    self.focus_previous()
                    return True
            self.focus_next()
        elif key == KEY_UP:
            self.focus_previous()
        elif key == KEY_DOWN:
            self.focus_next()
        elif key == KEY_ENTER:
            self.execute()
        return True

    def get_current_focus_idx(self):
        opt_idx = -1
        for idx, opt in enumerate(self.options):
            if opt.current_focus:
                opt_idx = idx
                break
        return opt_idx

    def get_current_focus_text(self):
        idx = self.get_current_focus_idx()
        if idx >= 0:
            return self.options[idx].text
        return None

    def focus_next(self):
        opt_idx = self.get_current_focus_idx()
        opt_idx = opt_idx + 1
        if opt_idx >= len(self.options):
            opt_idx = 0

        self.set_focus(opt_idx)

    def focus_previous(self):
        opt_idx = self.get_current_focus_idx()
        opt_idx = opt_idx - 1
        if opt_idx < 0:
            opt_idx = len(self.options) - 1
        self.set_focus(opt_idx)

    def set_focus(self, opt_idx):
        for idx in range(len(self.options)):
            f = (idx == opt_idx)
            self.options[idx].current_focus = f


class BmoMenu(Popup, JoystickHandler):
    def __init__(self, title: str, menu_items: list[str], callback: Callable, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.8)
        self.content = BmoMenuOptions(menu_items)
        self._menu_callback = callback
        Window.bind(on_key_down=self.on_key_down)
        self.bind(on_dismiss=self.on_popup_dismiss)
        self.bind_joystick(self.on_joystick)
        self.content.set_focus(0)

    def on_popup_dismiss(self, instance):
            self.unbind_joystick()

    def on_key_down(self, window, key, *args):
        if key in [KEY_TAB, KEY_UP, KEY_DOWN]:
            return self.content.on_key_down(window, key, *args)
        elif key == KEY_ENTER:
            return self._selected()
        return False

    def on_joystick(self, stick_id, action):
        if action == JOY_ACTION_A_BUTTON_DOWN:
            return self._selected()
        elif action == JOY_ACITON_ARROW_UP:
            self.content.focus_previous()
        elif action == JOY_ACTION_ARROW_DOWN:
            self.content.focus_next()
        elif action == JOY_ACTION_SELECT_BUTTON_DOWN:
            self._select_text(self.content.options[0].text)
        return True

    def _selected(self):
        text = self.content.get_current_focus_text()
        self._select_text(text)
        return True

    def _select_text(self, text):
        self._menu_callback(text)
        self.dismiss()

