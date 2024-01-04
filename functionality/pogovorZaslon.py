import threading

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField

from .api import poslji_gpt_api
from .pogovor import upravitelj_pogovorov
from .sporocilo import Sporocilo, SporociloWidget

pozdravno_sporocilo = '''Dobrodošli v GPT aplikaciji!
Sem GPT pomočnik, tukaj da vam pomagam.
Prosim, povejte mi, kako sem lahko danes v pomoč?'''


class PogovorZaslon(MDScreen):
    """
    razred tipa MDScreen, ki omogoci prikaz sporocil pogovora 
    """

    def spremeni_pogovor(self, pogovor_id):
        """
        nalozi pogovor glede na pogovor_id

        Parametri:
        - pogovor_id (int): id pogovora za nalaganje
        """
        self.pogovor = upravitelj_pogovorov.dobi_pogovor(pogovor_id)

    def posodobi_sporocila(self):
        """
        posodobi prikazana sporcila na pogovornem zaslonu
        """
        sporocila_view = self.ids["sporocila_box"]
        sporocila_view.clear_widgets()

        # prikazi pozdravno GUI sporocilo (pogovor je nov)
        pogovor_je_nov = self.pogovor.preveri_nov_pogovor()
        if pogovor_je_nov:
            uvodno_sporocilo = SporociloWidget(odgovor=pozdravno_sporocilo)
            uvodno_sporocilo.odgovor_se_nalaga = False
            sporocila_view.add_widget(uvodno_sporocilo)
            return

        # prikazi GUI sporocila (pogovor ze ima sporocila)
        for sporocilo in self.pogovor:
            sporocilo_widget = SporociloWidget(vprasanje=sporocilo.vprasanje,
                                               odgovor=sporocilo.odgovor,
                                               casovni_zig=sporocilo.casovni_zig)
            sporocila_view.add_widget(sporocilo_widget)

        sporocila_scroll = self.ids["sporocila_sv"]
        sporocila_scroll.scroll_y = 1.0

    def poslji_sporocilo_gpt(self, sporocilo):
        """
        poslji sprocoilo (vprasanje) na GPT API in posodobi pogovor

        Parametri:
        - sporocilo (Sporocilo): objekt tipa Sporocilo (ima vprasanje, nima odgovora) 
        """
        api_sporocila = self.pogovor.pripravi_api_sporocila()
        api_odgovor = poslji_gpt_api(api_sporocila)
        sporocilo.odgovor_se_nalaga = False
        sporocilo.odgovor = api_odgovor

        Clock.schedule_once(lambda x: self.posodobi_sporocila(), 0.125)

    def poslji_sporocilo(self):
        """
        poslje uporabnikovo sporocilo (vprasanje) na GPT API
        """
        vnosno_polje = self.ids["vnosno_polje"]
        vnosno_sporocilo = vnosno_polje.text.strip()
        if vnosno_sporocilo:
            vnosno_polje.text = ""
            novo_sporocilo = Sporocilo(vprasanje=vnosno_sporocilo)
            self.pogovor.dodaj_sporocilo(novo_sporocilo)
            self.posodobi_sporocila()

            api_nit = threading.Thread(
                target=self.poslji_sporocilo_gpt, args=(novo_sporocilo,))
            api_nit.start()

    def preimenuj_dialog_potrdi(self, novo_ime_pogovora):
        """
        nastavi ime pogovora na novo_ime_pogovora

        Parametri:
        - novo_ime_pogovora (str): novo ime pogovora
        """
        novo_ime_pogovora = novo_ime_pogovora.strip()
        if novo_ime_pogovora:
            self.pogovor.spremeni_ime(novo_ime_pogovora)
            self.ids["pogovor_naslov"].title = self.pogovor.ime
            self.preimenuj_dialog.dismiss()

    def prikazi_dialog_preimenuj(self, *args, **kwargs):
        """
        prikazi pojavno okno za preimenovanje pogovora
        """
        preimenujVnosnoPolje = MDTextField(
            text=self.pogovor.ime, required=True, error_color="indianred")
        zapriGumb = MDFlatButton(
            text="Prekliči", on_release=lambda x: self.preimenuj_dialog.dismiss())
        potrdiGumb = MDFlatButton(
            text="Potrdi", on_release=lambda x: self.preimenuj_dialog_potrdi(preimenujVnosnoPolje.text))

        self.preimenuj_dialog = MDDialog(
            title="Preimenuj pogovor",
            type="custom",
            content_cls=preimenujVnosnoPolje,
            buttons=[zapriGumb, potrdiGumb]
        )

        self.preimenuj_dialog.open()

    def zbrisi_dialog_potrdi(self):
        """
        zbrisi prikazan pogovor
        """
        upravitelj_pogovorov.zbrisi_pogovor(self.pogovor.id)
        self.zbrisi_dialog.dismiss()
        self.zamenjaj_zaslon_pogovori()

        # prikazi sporocilo - uspesno izbrisan pogovor (na zacetnem zaslonu)
        uZ = self.parent

        zz = uZ.get_screen("zacetniZaslon")
        zz.prikazi_obvestilo(
            f'Pogovor "{self.pogovor.ime}" je bil uspešno izbrisan!')

    def prikazi_dialog_zbrisi(self, *args, **kwargs):
        """
        prikazi pojavno okno za brisanje pogovora
        """
        zapriGumb = MDFlatButton(
            text="Prekliči", on_release=lambda x: self.zbrisi_dialog.dismiss())
        potrdiGumb = MDFlatButton(
            text="Potrdi", on_release=lambda x: self.zbrisi_dialog_potrdi())

        self.zbrisi_dialog = MDDialog(
            title="Izbris pogovora",
            text=f'Želiš zbrisati pogovor: {self.pogovor.ime}?',
            buttons=[zapriGumb, potrdiGumb]
        )

        self.zbrisi_dialog.open()

    def zamenjaj_zaslon_pogovori(self, *args, **kwargs):
        """
        spremeni zaslon na "zacetniZaslon" (pojdi nazaj na vse pogovore)
        """
        uZ = self.parent
        uZ.zamenjaj_zaslon("zacetniZaslon")

    def on_enter(self):
        """
        nalozi pogovor (sporocila), ko se zaslon odpre
        """
        self.ids["pogovor_naslov"].title = self.pogovor.ime
        self.posodobi_sporocila()

        uZ = self.parent
        uZ.zamenjaj_smer_prehoda()
