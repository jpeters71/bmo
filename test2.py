from kivy.app import App
from kivy.lang import Builder

from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.videoplayer import VideoPlayer

kv = """

BoxLayout:
    id: mainbox
    orientation: 'vertical'
    BoxLayout:
        id: vid
        rotation: 90
        on_touch_down: app.touch()


"""
class VApp(App):
    def build(self):
        build = Builder.load_string(kv)
        return build
    def on_start(self):
        self.c = VideoPlayer(source = '/home/bmo/work/media/adventure time.s02e26.mkv', fullscreen = True)
        self.root.ids.vid.add_widget(self.c)
    def touch(*args):
        print(args)
    def rotate(self):
        self.root.roataion = 90

if __name__ == "__main__":
    VApp().run()