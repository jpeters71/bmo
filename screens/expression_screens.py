from ast import Expression
import os
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from lib.bmo_player import BmoPlayer
from kivy.uix.video import Video
from kivy.logger import Logger

from lib.event_queue import BmoEvent, add_event
from screens.video_screen import VideoScreen


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

class ExpressionScreen(VideoScreen):
    def __init__(self, **kwargs):
        self._expression_name = kwargs.pop('expression_name')
        super().__init__(**kwargs)
        self._bgbox = MDBoxLayout(md_bg_color='#79C899')
        self._player = Video(allow_stretch=True, keep_ratio=True, size_hint_y=1)
        self._bgbox.add_widget(self._player)
        self.add_widget(self._bgbox)
        self.set_video_file(f'{ROOT_DIR}/../media/expressions/{self._expression_name}.mp4')
        self._player.bind(state=self.on_state)

    def on_state(self, instance, value):
        if value == 'stop':
            add_event(BmoEvent('expression_done', {'expression': self._expression_name}))


class DontKnowScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-do-not-understand', **kwargs)


class TryToDoThatScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='ok-i-will-try-to-do-that', **kwargs)


class GoodMorningScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-morning', **kwargs)


class GoodAfternoonScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-afternoon', **kwargs)


class GoodEveningScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-evening', **kwargs)
