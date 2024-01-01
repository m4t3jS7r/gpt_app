from kivy.lang import Builder
from kivymd.app import MDApp

from functionality.zacetniZaslon import ZacetniZaslon
from functionality.pogovorZaslon import PogovorZaslon
from functionality.upravljalecZaslonov import UpravljalecZaslonov


class gptApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("ui.kv")


if __name__ == "__main__":
    gptApp().run()
