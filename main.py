import os
from datetime import datetime

from kivy.config import Config
from lib.games.lightcycles import LightCyclesScreen
from screens.admin_screens import ListeningScreen, MainScreen
from screens.expression_screens import (
    DontKnowScreen,
    GoodAfternoonScreen,
    GoodEveningScreen,
    GoodMorningScreen,
    TryToDoThatScreen,
)
from screens.video_screen import VideoScreen

Config.read('./app_settings.ini')

from os import path

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp
from lib.event_queue import BmoEvent, add_event, get_next_event
from lib.games.pong import PongGame, PongScreen
from lib.games.snake import SnakeScreen
from lib.games.tetris import TetrisGame, TetrisScreen
from lib.listener import start_listening

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

# Builder.load_file('main.kv')


# Screen names
class ScreenNames:
    main = 'main'
    video = 'video'
    listening = 'listening'
    dont_know = 'dont_know'
    try_to_do_that = 'try_to_do_that'
    good_morning = 'good_morning'
    good_afternoon = 'good_afternoon'
    good_evening = 'good_evening'
    pong = 'pong'
    tetris = 'tetris'
    snake = 'snake'
    lightcycles = 'ligtcycles'


# Create the App class
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.material_style = 'M3'
        self._app_name = 'BMO'
        Window.show_cursor = False
        self._title = 'BMO'
        self._listener_thread = start_listening(ROOT_DIR)
        self._previous_screen = None

        # Setup screens
        self._sm = ScreenManager(transition=NoTransition())

        self._sm.add_widget(MainScreen(name=ScreenNames.main))
        self._video_screen = VideoScreen(name=ScreenNames.video)
        self._sm.add_widget(self._video_screen)
        self._sm.add_widget(ListeningScreen(name=ScreenNames.listening))
        self._sm.add_widget(DontKnowScreen(name=ScreenNames.dont_know))
        self._try_screen = TryToDoThatScreen(name=ScreenNames.try_to_do_that)
        self._sm.add_widget(self._try_screen)
        self._sm.add_widget(GoodMorningScreen(name=ScreenNames.good_morning))
        self._sm.add_widget(GoodAfternoonScreen(name=ScreenNames.good_afternoon))
        self._sm.add_widget(GoodEveningScreen(name=ScreenNames.good_evening))
        self._sm.add_widget(SnakeScreen(name=ScreenNames.snake))
        self._sm.add_widget(TetrisScreen(name=ScreenNames.tetris))

        self._pong_game = PongScreen(name=ScreenNames.pong)
        self._sm.add_widget(self._pong_game)

        self._sm.add_widget(LightCyclesScreen(name=ScreenNames.lightcycles))

        return self._sm

    def on_start(self):
        self._ev_clock = Clock.schedule_interval(self._process_events, 0.5)
        add_event(BmoEvent('startup', {}))

    def _process_events(self, dt):
        # Check for events
        ev = get_next_event()
        if ev:
            Logger.info(f'Processing event: {ev.event_name} with data {ev.event_data}')
            ev_data = ev.event_data or {}
            if ev.event_name == 'wake_word':
                Logger.info('Handling wake word in main')
                if self._sm.current == ScreenNames.video:
                    self._video_screen.pause()
            elif ev.event_name == 'unknown_command':
                self.unknown()
            elif ev.event_name == 'startup':
                # For testing only
                # self._sm.current = ScreenNames.tetris

                self._startup()
            elif ev.event_name == 'leave_screen':
                self._sm.current = ScreenNames.main
            elif ev.event_name == 'expression_done':
                self._switch_screens(ScreenNames.main)
            elif ev.event_name == 'play_video':
                if self._sm.current != ScreenNames.video:
                    if ev.event_data.get('prequel_done'):
                        # Build up filename
                        season = ev_data.get('season')
                        episode = ev_data.get('episode')
                        pth = path.expanduser(f'~/work/media/adventure time.s{season:02}e{episode:02}.mkv')
                        self._video_screen.set_video_file(pth)
                        self._sm.current = ScreenNames.video
                    else:
                        self.try_to_do_that(ev)
                else:
                    # Resume
                    self._video_screen.play()
            elif ev.event_name == 'play_video_no_prequel':
                pth = ev_data.get('file')
                self._video_screen.set_video_file(pth)
                self._sm.current = ScreenNames.video
            elif ev.event_name == 'pause':
                self._video_screen.pause()
            elif ev.event_name == 'stop':
                Logger.info('Processing stop...')
                self._video_screen.stop()

            # Games
            elif ev.event_name == 'play_game':
                game_name = ev_data.get('game')
                Logger.info(f'Play game [{game_name}]')

                if game_name == 'pong':
                    self._sm.current = ScreenNames.pong
                    self._pong_game.play()
                elif game_name == 'tetris':
                    self._game_widget = TetrisGame()
                    self._layout.remove_widget(self._image)
                    self._layout.add_widget(self._game_widget)

                elif game_name == 'snake':
                    self._game_widget = SnakeGame()
                    self._layout.remove_widget(self._image)
                    self._layout.add_widget(self._game_widget)

    def listen(self):
        self._previous_screen = self._sm.current
        self._sm.current = ScreenNames.listening

    def unlisten(self):
        if not self._previous_screen:
            self._sm.current = self._previous_screen
            self._previous_screen = None

    def unknown(self):
        self._sm.current = ScreenNames.dont_know

    def try_to_do_that(self, ev: BmoEvent):
        ev.event_data['prequel_done'] = True
        self._try_screen.set_leave_event(ev)
        self._sm.current = ScreenNames.try_to_do_that

    def _switch_screens(self, screen_name: str):
        self._sm.current = screen_name

    def _startup(self):
        # Check the time to figure out what time of day it is
        now = datetime.now()
        hour = now.hour
        if 6 <= hour < 12:
            self._switch_screens(ScreenNames.good_morning)
        elif 12 <= hour < 18:
            self._switch_screens(ScreenNames.good_afternoon)
        else:
            self._switch_screens(ScreenNames.good_evening)


# run the app
sample_app = MainApp()
sample_app.run()
