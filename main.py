import os
from kivy.config import Config

from lib.event_queue import get_next_event
from lib.listener import start_listening

Config.read('./app_settings.ini')

from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.logger import Logger

from os import path
import random


kv = """

BoxLayout:
    id: mainbox
    orientation: 'vertical'
    BoxLayout:
        id: vid
        rotation: 270


"""
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title = 'Simple Video'
        self._images = [path.join(f'{ROOT_DIR}/media/faces', f) for f in os.listdir(f'{ROOT_DIR}/media/faces') if f.endswith('.jpg')]
        self._listener_thread = start_listening(ROOT_DIR)

    def build(self):
        # self.theme_cls.theme_style = 'Dark'
        # self.theme_cls.primary_palette = 'BlueGray'
        # build = Builder.load_string(kv)
        self._layout = BoxLayout()
        self._image = Image(source=f'{ROOT_DIR}/media/faces/bmo00.jpg', allow_stretch=True)
        self._layout.add_widget(self._image)

        return self._layout

    def on_start(self):
        # pth = path.expanduser('~/work/media/adventure time.s01e02.mkv')
        # self.player = VideoPlayer(source=pth)
        # self.player.state = 'play'
        # self.player.options = {
        #     'eos': 'stop',
        # }
        # self._layout.add_widget(self.player)
        self._ev_clock = Clock.schedule_interval(self._process_events, 5)
        pass

    def touch(*args):
        print(args)

    # def rotate(self):
    #     self.root.rotation = 270

    def _process_events(self, dt):
        # Check for events
        ev = get_next_event()
        if ev:
            Logger.info(f'Processing event: {ev.event_name} with data {ev.event_data}')
            ev_data = ev.event_data or {}
            if ev.event_name == 'play_video':
                # Build up filename
                self._ev_clock.cancel()
                self._ev_clock = None
                season = ev_data.get('season')
                episode = ev_data.get('episode')
                pth = path.expanduser(f'~/work/media/adventure time.s{season:02}e{episode:02}.mkv')
                self._player = VideoPlayer(source=pth)
                self._player.state = 'play'
                self._player.options = {
                     'eos': 'stop',
                }
                self._layout.remove_widget(self._image)
                self._layout.add_widget(self._player)



MainApp().run()
