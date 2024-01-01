# import json
import time
from kivy.clock import Clock
from urllib.parse import quote, unquote
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ObjectProperty, ColorProperty


class SporociloWidget(MDBoxLayout):
    vprasanje = StringProperty()
    odgovor = StringProperty()

    def __init__(self, vprasanje='', odgovor='', casovni_zig=False, **kwargs):
        super(SporociloWidget, self).__init__(**kwargs)
        self.vprasanje = vprasanje
        self.odgovor = odgovor
        self.casovni_zig = casovni_zig or time.strftime(
            "%Y.%m.%d - %H:%M", time.localtime())
        # ce vprasanje se nima odgovora -> odgovor_se_nalaga = True
        self.odgovor_se_nalaga = not (vprasanje and odgovor)

        # ce vprasanje se nima odgovora, prikazi nalaganje (nalagalne pike)
        Clock.schedule_once(self.animacija_odgovor, 0.5)
        # print(self.height)
        # self.height = self.children[0]True.texture_size[1] + self.children[1].texture_size[1]

    def zrcali_text(self, vsebina):
        vrstice = vsebina.split('\n')
        zrcaljene_vrstice = reversed(vrstice)
        zrcaljene_vsebina = "\n".join(zrcaljene_vrstice)
        return zrcaljene_vsebina

    def animacija_odgovor(self, *args, **kwargs):
        if self.odgovor_se_nalaga:
            Clock.schedule_once(self.animacija_odgovor, 0.5)

            stevilo_pik = len(self.odgovor)
            if stevilo_pik == 3:
                self.odgovor = ""
            else:
                self.odgovor += "."


class Sporocilo:
    def __init__(self, vprasanje=False, odgovor=False, casovni_zig=False):
        self.vprasanje = vprasanje or ''
        self.odgovor = odgovor or ''
        _casovni_zig = casovni_zig or time.strftime(
            "%Y.%m.%d - %H:%M", time.localtime())
        self.casovni_zig = _casovni_zig
        pass

    def to_dict(self):
        return {'vprasanje': self.vprasanje, 'odgovor': self.odgovor,
                'casovni_zig': self.casovni_zig}

    def to_api_list(self):
        return [
            {"role": "assistant", "content": self.odgovor or "odgovarjam v slovenščini"},
            {"role": "user", "content": self.vprasanje}
        ]

    @classmethod
    def from_dict(cls, dict):
        sporocilo = cls()
        sporocilo.casovni_zig = dict['casovni_zig']
        sporocilo.vprasanje = dict['vprasanje']
        sporocilo.odgovor = dict['odgovor']
        return sporocilo
