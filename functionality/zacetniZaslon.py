from kivy.clock import Clock
from functools import partial


from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.list import IconLeftWidgetWithoutTouch

from .pogovor import upravitelj_pogovorov


class ZacetniZaslon(MDScreen):
    """
    zacetni razred tipa MDScreen, ki omogoci usvarjanje in prikaz pogovorov
    """

    def zacni_pogovor(self, *args, **kwargs):
        """
        funkicja ki se zažene, ko je pritisnjen gumb za nov pogovor 
        """
        nov_pogovor_id = upravitelj_pogovorov.ustvari_nov_pogovor()
        uZ = self.parent
        pZ = uZ.get_screen("pogovorZaslon")
        pZ.spremeni_pogovor(nov_pogovor_id)
        uZ.zamenjaj_zaslon("pogovorZaslon")

    def prikazi_obvestilo(self, obvestilo_text):
        """
        prikazi obvestiko (toast) z vsebino obvestilo_text

        Parametri:
        - obvestilo_text (str): sporocilo za prikaz
        """
        toast(obvestilo_text)

    def prikazi_uvodno_sporocilo(self, je_vidno):
        """
        prikazi ali skrij uvodno sporocilo

        Parametri:
        - je_vidno (bool): določi vidnost uvodnega sporocila
        """
        prikazi_sporocilo = int(je_vidno)
        self.ids.uvodno_sporocilo.opacity = prikazi_sporocilo
        self.ids.uvodno_sporocilo.size_hint = (
            prikazi_sporocilo, prikazi_sporocilo)

    def prikazi_pogovor(self, pogovor_id, *args, **kwargs):
        """
        prikazi dolocen pogovor, ko je izbran

        Parametri:
        - pogovor_id (int): id pogovora za prikaz
        """
        uZ = self.parent
        pZ = uZ.get_screen("pogovorZaslon")
        pZ.spremeni_pogovor(pogovor_id)
        uZ.zamenjaj_zaslon("pogovorZaslon")

    def prikazi_pogovore(self, pogovori, *args, **kwargs):
        """
        prikazi seznam pogovorov na zaslonu

        Parametri:
        - pogovori (seznam): seznam objektov tipa Pogovor
        """
        self.ids.pogovori_list.clear_widgets()
        for pogovor in pogovori:
            on_release_fun = partial(self.prikazi_pogovor, pogovor.id)
            self.ids.pogovori_list.add_widget(OneLineIconListItem(
                IconLeftWidgetWithoutTouch(icon="forum-outline"),
                on_release=on_release_fun,
                text=f'{pogovor.ime}'))

    def nalozi_pogovore(self, *args, **kwargs):
        """
        nalozi in prikazi pogovore, ko se zaslon nalaga
        """
        self.pogovori = upravitelj_pogovorov.dobi_pogovore()
        self.prikazi_pogovore(pogovori=self.pogovori)

        # zacento_stanje -> true, ko ni pogovorov
        zacento_stanje = len(self.pogovori) == 0
        self.prikazi_uvodno_sporocilo(zacento_stanje)

    def on_enter(self, *args, **kwargs):
        """
        izvrsi nalaganje pogovorov, ko se zaslon odpre
        """
        Clock.schedule_once(self.nalozi_pogovore, 0.125)

        uZ = self.parent
        uZ.zamenjaj_smer_prehoda()
