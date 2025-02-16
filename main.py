from calendar import c
import os
from datetime import datetime
import random

from kivy.config import Config
from lib.games.lightcycles import LightCyclesScreen
from lib.volume import VolumeLevel, set_volume_level
from screens.admin_screens import ListeningScreen, MainScreen
from screens.expression_screens import (
    CongratulationsToMeScreen,
    CongratulationsToPlayerOneScreen,
    CongratulationsToPlayerTwoScreen,
    DidntHearYouScreen,
    DoTodayScreen,
    DontKnowScreen,
    FunSoonScreen,
    GoodAfternoonScreen,
    GoodByeScreen,
    GoodEveningScreen,
    GoodMorningScreen,
    GoodPersonScreen,
    IAmBoredScreen,
    IAmTiredScreen,
    ItIsLateScreen,
    LoveYouScreen,
    MissYouScreen,
    PlayGamesScreen,
    PlayShowsScreen,
    SleepNowScreen,
    ThisOkScreen,
    TryToDoThatScreen,
    WasThatFunScreen,
)
from screens.video_screen import VideoScreen
from screens.weather_screen import WeatherScreen

Config.read('./app_settings.ini')

from os import path

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.uix.screenmanager import NoTransition, ScreenManager
from kivymd.app import MDApp
from lib.event_queue import BmoEvent, add_event, get_next_event
from lib.games.pong import PongScreen
from lib.games.snake import SnakeScreen
from lib.games.tetris import TetrisScreen
from lib.listener import start_listening

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


# Screen names
class ScreenNames:
    # Admin screens
    main = 'main'
    video = 'video'
    listening = 'listening'

    # Expressions
    congratulations_to_me = 'congratulations_to_me'
    congratulations_to_player_one = 'congratulations_to_player_one'
    congratulations_to_player_two = 'congratulations_to_player_two'
    didnt_hear = 'didnt_hear'
    do_today = 'do_today'
    dont_know = 'dont_know'
    fun_soon = 'fun_soon'
    good_afternoon = 'good_afternoon'
    good_bye = 'good_bye'
    good_evening = 'good_evening'
    good_morning = 'good_morning'
    good_person = 'good_person'
    i_am_bored = 'i_am_bored'
    i_am_tired = 'i_am_tired'
    it_is_late = 'it_is_late'
    love_you = 'love_you'
    miss_you = 'miss_you'
    play_games = 'play_games'
    play_shows = 'play_shows'
    sleep_now = 'sleep_now'
    this_ok = 'this_ok'
    try_to_do_that = 'try_to_do_that'
    was_that_fun = 'was_that_fun'
    watch_show = 'watch_show'
    weather = 'weather'

    # Games
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

        # Expressions
        self._sm.add_widget(CongratulationsToMeScreen(name=ScreenNames.congratulations_to_me))
        self._sm.add_widget(CongratulationsToPlayerOneScreen(name=ScreenNames.congratulations_to_player_one))
        self._sm.add_widget(CongratulationsToPlayerTwoScreen(name=ScreenNames.congratulations_to_player_two))
        self._sm.add_widget(DidntHearYouScreen(name=ScreenNames.didnt_hear))
        self._sm.add_widget(DoTodayScreen(name=ScreenNames.do_today))
        self._sm.add_widget(DontKnowScreen(name=ScreenNames.dont_know))
        self._sm.add_widget(FunSoonScreen(name=ScreenNames.fun_soon))
        self._sm.add_widget(GoodAfternoonScreen(name=ScreenNames.good_afternoon))
        self._sm.add_widget(GoodByeScreen(name=ScreenNames.good_bye))
        self._sm.add_widget(GoodEveningScreen(name=ScreenNames.good_evening))
        self._sm.add_widget(GoodMorningScreen(name=ScreenNames.good_morning))
        self._sm.add_widget(GoodPersonScreen(name=ScreenNames.good_person))
        self._sm.add_widget(IAmBoredScreen(name=ScreenNames.i_am_bored))
        self._sm.add_widget(IAmTiredScreen(name=ScreenNames.i_am_tired))
        self._sm.add_widget(ItIsLateScreen(name=ScreenNames.it_is_late))
        self._sm.add_widget(LoveYouScreen(name=ScreenNames.love_you))
        self._sm.add_widget(MissYouScreen(name=ScreenNames.miss_you))
        self._sm.add_widget(PlayGamesScreen(name=ScreenNames.play_games))
        self._sm.add_widget(PlayShowsScreen(name=ScreenNames.play_shows))
        self._sm.add_widget(SleepNowScreen(name=ScreenNames.sleep_now))
        self._sm.add_widget(ThisOkScreen(name=ScreenNames.this_ok))
        self._try_screen = TryToDoThatScreen(name=ScreenNames.try_to_do_that)
        self._sm.add_widget(self._try_screen)
        self._sm.add_widget(WasThatFunScreen(name=ScreenNames.was_that_fun))
        self._sm.add_widget(WeatherScreen(name=ScreenNames.weather))

        # Games
        self._sm.add_widget(SnakeScreen(name=ScreenNames.snake))
        self._sm.add_widget(TetrisScreen(name=ScreenNames.tetris))
        self._sm.add_widget(PongScreen(name=ScreenNames.pong))
        self._sm.add_widget(LightCyclesScreen(name=ScreenNames.lightcycles))

        return self._sm

    def on_start(self):
        set_volume_level(VolumeLevel.medium)
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
                self._startup()
            elif ev.event_name == 'leave_screen':
                self._leave_screen(ev_data)
            elif ev.event_name == 'expression_done':
                self._switch_screens(ScreenNames.main)
            elif ev.event_name == 'play_video':
                if self._sm.current != ScreenNames.video:
                    if ev.event_data.get('prequel_done'):
                        # Build up filename
                        show = ev_data.get('show')
                        season = ev_data.get('season')
                        episode = ev_data.get('episode')
                        pth = path.expanduser(f'~/work/media/{show}.s{season:02}e{episode:02}.mkv')

                        if not os.path.exists(pth):
                            Logger.error(f'File not found: {pth}')
                            self.unknown()
                        else:
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
                elif game_name == 'tetris':
                    self._sm.current = ScreenNames.tetris
                elif game_name == 'snake':
                    self._sm.current = ScreenNames.snake
                elif game_name == 'lightcycles':
                    self._sm.current = ScreenNames.lightcycles

            # Exit
            elif ev.event_name == 'exit':
                if ev.event_data.get('prequel_done'):
                    Logger.info('Exiting...')
                    self.stop()
                else:
                    self.prequel_screen(ScreenNames.good_bye, ev)
            elif ev.event_name == 'show_weather':
                if ev.event_data.get('prequel_done'):
                    self._sm.current = ScreenNames.weather
                else:
                    self.try_to_do_that(ev)

    def listen(self):
        self._previous_screen = self._sm.current
        self._sm.current = ScreenNames.listening

    def unlisten(self):
        if not self._previous_screen:
            self._sm.current = self._previous_screen
            self._previous_screen = None

    def unknown(self):
        # Randomly select an unknown screen
        scr = random.choice([ScreenNames.dont_know, ScreenNames.dont_know, ScreenNames.dont_know, ScreenNames.didnt_hear])
        self._sm.current = scr

    def try_to_do_that(self, ev: BmoEvent):
        self.prequel_screen(ScreenNames.try_to_do_that, ev)

    def prequel_screen(self, prequel_screen: str, ev: BmoEvent):
        ev.event_data['prequel_done'] = True
        scrn = self._sm.get_screen(prequel_screen)
        scrn.set_leave_event(ev)
        self._sm.current = prequel_screen

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

    def _leave_screen(self, ev_data: dict):
        if ev_data.get('type') == 'game':
            # Randomly select a screen we might want to show
            scrs = [ScreenNames.main, ScreenNames.main, ScreenNames.main, ScreenNames.was_that_fun, ScreenNames.play_games]
            winner = ev_data.get('winner') or ''
            if winner == 'player1':
                scrs.extend(
                    [
                        ScreenNames.congratulations_to_player_one,
                        ScreenNames.congratulations_to_player_one,
                        ScreenNames.congratulations_to_player_one,
                    ]
                )
            elif winner == 'player2':
                scrs.extend(
                    [
                        ScreenNames.congratulations_to_player_two,
                        ScreenNames.congratulations_to_player_two,
                        ScreenNames.congratulations_to_player_two,
                    ]
                )
            elif winner == 'computer':
                scrs.extend(
                    [ScreenNames.congratulations_to_me, ScreenNames.congratulations_to_me, ScreenNames.congratulations_to_me]
                )

            scr = random.choice(scrs)
            self._sm.current = scr
        else:
            self._sm.current = ScreenNames.main


if __name__ == '__main__':
    MainApp().run()
