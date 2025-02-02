import os
from kivymd.uix.boxlayout import MDBoxLayout

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


# Expresssion Screen classes
class CongratulationsToMeScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='congratulations-to-me', **kwargs)


class CongratulationsToPlayerOneScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='congratulations-to-player-one', **kwargs)


class CongratulationsToPlayerTwoScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='congratulations-to-player-two', **kwargs)


class DidntHearYouScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='huh-i-didnt-hear-you', **kwargs)


class DoTodayScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='what-do-you-want-to-do-today', **kwargs)


class DontKnowScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-do-not-understand', **kwargs)


class FunSoonScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-hope-we-do-something-fun-soon', **kwargs)


class GoodAfternoonScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-afternoon', **kwargs)


class GoodByeScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-bye', **kwargs)


class GoodEveningScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-evening', **kwargs)


class GoodMorningScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='good-morning', **kwargs)


class GoodPersonScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='you-are-a-good-person', **kwargs)


class IAmBoredScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-am-bored', **kwargs)


class IAmTiredScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-am-so-tired', **kwargs)


class ItIsLateScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='it-is-late', **kwargs)


class LoveYouScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-love-you', **kwargs)


class MissYouScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-will-miss-you', **kwargs)


class PlayGamesScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='who-wants-to-play-video-games', **kwargs)


class PlayShowsScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='who-wants-to-watch-a-show', **kwargs)


class SleepNowScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='i-will-go-to-sleep-now', **kwargs)


class ThisOkScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='is-this-ok', **kwargs)


class TryToDoThatScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='ok-i-will-try-to-do-that', **kwargs)


class WasThatFunScreen(ExpressionScreen):
    def __init__(self, **kwargs):
        super().__init__(expression_name='was-that-fun', **kwargs)
