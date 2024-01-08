import threading

from kivy.clock import Clock
from kivy.utils import platform

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField


from .api import poslji_gpt_api
from .pogovor import upravitelj_pogovorov
from .sporocilo import Sporocilo, SporociloWidget

pozdravno_sporocilo = '''Dobrodošli v GPT aplikaciji! Sem vaš pomočnik GPT. Kako vam lahko danes pomagam?'''


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

    def posodobi_sporocila(self, *args, **kwargs):
        """
        posodobi prikazana sporcila na pogovornem zaslonu
        """
        sporocila_view = self.ids["sporocila_box"]
        sporocila_view.clear_widgets()

        # nastavi UI elemente na zacetno stanje
        poslji_gumb = self.ids["poslji_gumb"]
        poslji_gumb.icon = "send-outline"
        vnosno_polje = self.ids["vnosno_polje"]
        vnosno_polje.text = ""
        vnosno_polje.focus = False
        vnosno_polje.hint_text = "Vnesi svoje sporocilo..."

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

        upravitelj_pogovorov.shrani_v_db()
        Clock.schedule_once(self.posodobi_sporocila, 0.125)

    def novo_sporocilo(self):
        """
        koda se izvedo po kliku na gumb poslji (oz. preimenuj)
            -> poslji uporabnikovo sporocilo (vprasanje) na GPT API
            -> spremeni ime pogovora
        """
        vnosno_polje = self.ids["vnosno_polje"]
        poslji_gumb = self.ids["poslji_gumb"]

        vnosno_sporocilo = vnosno_polje.text.strip()
        if vnosno_sporocilo:
            if poslji_gumb.icon == "send-outline":
                # vneseno sporocilo je namenjeno za GPT API
                novo_sporocilo = Sporocilo(vprasanje=vnosno_sporocilo)
                self.pogovor.dodaj_sporocilo(novo_sporocilo)

                api_nit = threading.Thread(
                    target=self.poslji_sporocilo_gpt, args=(novo_sporocilo,))
                api_nit.start()
            else:
                # vneseno sporocilo je novo ime pogovora
                self.nastavi_ime_pogovora(vnosno_sporocilo)

            Clock.schedule_once(self.posodobi_sporocila, 0.125)


    def nastavi_ime_pogovora(self, novo_ime_pogovora):
        """
        spremeni ime pogovora na novo_ime_pogovora
        Parametri:
        - novo_ime_pogovora (str): novo ime pogovora
        """
        novo_ime_pogovora = novo_ime_pogovora.strip()

        if novo_ime_pogovora:
            self.pogovor.spremeni_ime(novo_ime_pogovora)
            self.ids["pogovor_naslov"].title = self.pogovor.ime

            # ce ni android, zapri dialog
            try:
                self.preimenuj_dialog.dismiss()
            except AttributeError as e:
                pass

    def preimenuj_pogovor(self, *args, **kwargs):
        """
        spremeni UI v nacin za preimenovanje pogovora
        """
        if platform == "android":
            poslji_gumb = self.ids["poslji_gumb"]
            poslji_gumb.icon = "check-bold"

            vnosno_polje = self.ids["vnosno_polje"]
            vnosno_polje.hint_text = "Vnesi novo ime pogovora..."
            vnosno_polje.text = self.pogovor.ime
            vnosno_polje.focus = True

        else:
            preimenujVnosnoPolje = MDTextField(
                text=self.pogovor.ime, required=True, error_color="indianred")
            zapriGumb = MDFlatButton(
                text="Prekliči", on_release=lambda x: self.preimenuj_dialog.dismiss())
            potrdiGumb = MDFlatButton(
                text="Potrdi", on_release=lambda x: self.nastavi_ime_pogovora(preimenujVnosnoPolje.text))

            self.preimenuj_dialog = MDDialog(
                title="Preimenuj pogovor",
                type="custom",
                content_cls=preimenujVnosnoPolje,
                buttons=[zapriGumb, potrdiGumb]
            )

            self.preimenuj_dialog.open()

    def on_keyboard(self, focus, **kwargs):
        """
        spremeni UI, ko je vidna tipkovnica (android) 
            -> zamik sporocil proti dnu zaslona 
        """
        if platform == "android":
            sporocila_view = self.ids["sporocila_box"]

            if focus:
                sporocila_view.adaptive_height = False
                sporocila_view.height = sporocila_view.height + 750
            else:
                sporocila_view.height = sporocila_view.height - 750
                sporocila_view.adaptive_height = True

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
