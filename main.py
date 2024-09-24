import os
from kivy.config import Config

Config.read('./app_settings.ini')

from lib.event_queue import get_next_event
from lib.games.pong import PongGame
from lib.listener import start_listening

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.logger import Logger

from os import path


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.show_cursor = False
        self._title = 'Simple Video'
        self._images = [path.join(f'{ROOT_DIR}/media/faces', f) for f in os.listdir(f'{ROOT_DIR}/media/faces') if f.endswith('.jpg')]
        self._listener_thread = start_listening(ROOT_DIR)
        self._video_player = None
        self._game_widget = None

    def build(self):
        self._layout = BoxLayout()
        self._image = Image(source=f'{ROOT_DIR}/media/faces/bmo00.jpg', allow_stretch=True)
        self._layout.add_widget(self._image)

        return self._layout

    def on_start(self):
        self._ev_clock = Clock.schedule_interval(self._process_events, 5)


    def _process_events(self, dt):
        # Check for events
        ev = get_next_event()
        if ev:
            Logger.info(f'Processing event: {ev.event_name} with data {ev.event_data}')
            ev_data = ev.event_data or {}
            if ev.event_name == 'play_video':
                if not self._video_player:
                    # Build up filename
                    season = ev_data.get('season')
                    episode = ev_data.get('episode')
                    pth = path.expanduser(f'~/work/media/adventure time.s{season:02}e{episode:02}.mkv')
                    self._video_player = VideoPlayer(source=pth)
                    self._video_player.state = 'play'
                    self._video_player.options = {
                        'eos': 'stop',
                    }
                    self._layout.remove_widget(self._image)
                    self._layout.add_widget(self._video_player)
                else:
                    self._video_player.state = 'play'
            elif ev.event_name == 'pause':
                self._video_player.state = 'pause'
            elif ev.event_name == 'stop':
                self._video_player.state = 'stop'
                if self._video_player:
                    self._layout.remove_widget(self._video_player)
                    self._video_player = None
                    self._layout.add_widget(self._image)
            # Games
            elif ev.event_name == 'play_game':
                game_name = ev_data.get('game')
                Logger.info(f'Play game [{game_name}]')

                if game_name == 'pong':
                    self._game_widget = PongGame()
                    self._layout.remove_widget(self._image)
                    self._layout.add_widget(self._game_widget)



MainApp().run()
