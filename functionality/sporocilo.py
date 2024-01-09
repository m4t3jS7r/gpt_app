import time
from kivy.clock import Clock

from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty


class SporociloWidget(MDBoxLayout):
    """
    implementacija GUI komponente za sporocilo (funkcionalnost)
    """
    vprasanje = StringProperty()
    odgovor = StringProperty()

    def __init__(self, vprasanje='', odgovor='', casovni_zig=False, **kwargs):
        """
        ustvari nov objekt tipa Sporocilo (GUI komponenta)

        Parametri:
        - vprasanje (str): vprasanje
        - odgovor (str): odgovor
        - casovni_zig (str): unix casovni zig sporocila
        """
        # koda se zažene, ko se ustvari novo sporočilo (GUI element)
        super(SporociloWidget, self).__init__(**kwargs)
        self.vprasanje = vprasanje
        self.odgovor = odgovor
        self.casovni_zig = casovni_zig or time.strftime(
            "%Y.%m.%d - %H:%M", time.localtime())
        # ce vprasanje se nima odgovora -> odgovor_se_nalaga = True
        self.odgovor_se_nalaga = not (vprasanje and odgovor)

        # ce vprasanje se nima odgovora, prikazi nalaganje (nalagalne pike)
        Clock.schedule_once(self._animacija_odgovor, 0.5)

    def _animacija_odgovor(self, *args, **kwargs):
        """
        * interna funkcija *
        simuliraj nalaganje treh pik (odgovor)
        """
        if self.odgovor_se_nalaga:
            Clock.schedule_once(self._animacija_odgovor, 0.5)

            stevilo_pik = len(self.odgovor)
            if stevilo_pik == 3:
                self.odgovor = ""
            else:
                self.odgovor += "."


class Sporocilo:
    """
    implementacija razreda za sporocilo (funkcionalnost)
    """

    def __init__(self, vprasanje=False, odgovor=False, casovni_zig=False):
        """
        ustvari nov objekt tipa Sporocilo

        Parametri:
        - vprasanje (str): vprasanje
        - odgovor (str): odgovor
        - casovni_zig (str): unix casovni zig sporocila
        """
        # koda se zažene, ko se ustvari novo sporočilo
        self.vprasanje = vprasanje or ''
        self.odgovor = odgovor or ''
        _casovni_zig = casovni_zig or time.strftime(
            "%Y.%m.%d - %H:%M", time.localtime())
        self.casovni_zig = _casovni_zig

    def to_dict(self):
        """
        pretvori objekt tipa Sporocilo v knjizno obliko
        """
        # metoda uporabljena za shranjevanje sporocil
        return {'vprasanje': self.vprasanje, 'odgovor': self.odgovor,
                'casovni_zig': self.casovni_zig}

    def to_api_list(self):
        """
        vrne sporocilo (vprasanje & odgovor) kot seznam (GPT API oblika)
        """
        return [
            {"role": "assistant" if self.odgovor else "system",
                "content": self.odgovor or "You respond in Slovenian"},
            {"role": "user", "content": self.vprasanje}
        ]

    @classmethod
    def from_dict(cls, dict):
        """
        ustvari in vrne objekt tipa Sporocilo

        Parametri:
        - dict (dict): knjizna oblika sporocila 
        """
        # metoda uporabljena za nalaganje (obstojecih) sporocil
        sporocilo = cls()
        sporocilo.casovni_zig = dict['casovni_zig']
        sporocilo.vprasanje = dict['vprasanje']
        sporocilo.odgovor = dict['odgovor']
        return sporocilo
