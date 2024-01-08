from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.core.window import Window

from functionality.zacetniZaslon import ZacetniZaslon
from functionality.pogovorZaslon import PogovorZaslon
from functionality.upravljalecZaslonov import UpravljalecZaslonov


class gptApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("ui.kv")

    def on_start(self):
        Window.softinput_mode = 'pan'
        # Window.softinput_mode = 'below_target'


if __name__ == "__main__":
    gptApp().run()
