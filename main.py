from kivy.config import Config

Config.read('./app_settings.ini')

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.videoplayer import VideoPlayer
from os.path import expanduser


kv = """

BoxLayout:
    id: mainbox
    orientation: 'vertical'
    BoxLayout:
        id: vid
        rotation: 270


"""


class MainApp(MDApp):
    title = 'Simple Video'

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        build = Builder.load_string(kv)
        return build

    def on_start(self):
        pth = expanduser('~/work/media/adventure time.s01e02.mkv')
        self.player = VideoPlayer(source=pth)
        self.player.state = 'play'
        self.player.options = {
            'eos': 'stop',
        }
        self.root.ids.vid.add_widget(self.player)

    def touch(*args):
        print(args)

    def rotate(self):
        self.root.roataion = 270


MainApp().run()
