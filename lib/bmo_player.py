from kivy.logger import Logger
from kivy.uix.video import Video


class BmoPlayer(Video):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state='stop'
        self.options={}
        self.bind(on_touch_down = self.on_stop)

    def play_video(self, path):
        self.source = path
        self.state = 'play'

    def stop_video(self):
        self.state = 'stop'

    def check(self):
        Logger.info("film position:" + str(self.position))

    def on_stop(self,  *args):
        self.stop_video()
