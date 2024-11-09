from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout

from lib.bmo_player import BmoPlayer
from kivy.uix.video import Video
from kivy.logger import Logger


class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bgbox = MDBoxLayout()
        self._bgbox.background
        self._player = Video(allow_stretch=False, keep_ratio=False, size_hint_y=1)
        self._bgbox.add_widget(self._player)
        self.add_widget(self._bgbox)
        self._current_file = None

    def set_video_file(self, current_file: str):
        self._current_file = current_file

    def play(self):
        self._player.state='play'

    def pause(self):
        self._player.state='pause'

    def stop(self):
        self._player.state='stop'

    def on_enter(self):
        Logger.info('ENTER Video screen')
        self._player.source = self._current_file
        if self._player.loaded:
            self._player.seek(0.000)
        self.play()

    def on_leave(self):
        self._player.unload()

