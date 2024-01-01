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
    def spremeni_pogovor(self, pogovor_id):
        self.pogovor = upravitelj_pogovorov.dobi_pogovor(pogovor_id)
        # print(f'got {pogovor_id}')
        # self.posodobi_sporocila()

    def posodobi_sporocila(self):
        sporocila_view = self.ids["sporocila_box"]
        sporocila_view.clear_widgets()

        pogovor_je_nov = self.pogovor.preveri_nov_pogovor()
        if pogovor_je_nov:
            uvodno_sporocilo = SporociloWidget(odgovor=pozdravno_sporocilo)
            uvodno_sporocilo.odgovor_se_nalaga = False
            sporocila_view.add_widget(uvodno_sporocilo)
            return

        for sporocilo in self.pogovor:
            sporocilo_widget = SporociloWidget(vprasanje=sporocilo.vprasanje,
                                               odgovor=sporocilo.odgovor,
                                               casovni_zig=sporocilo.casovni_zig)
            sporocila_view.add_widget(sporocilo_widget)

        sporocila_scroll = self.ids["sporocila_sv"]
        sporocila_scroll.scroll_y = 1.0
        # if pojdi_na_vrh:
        # print(f'{sporocilo.vprasanje} - {sporocilo.odgovor}')

    # def posodobi_sporocila(self):
    #     for Sporocilo in self.Pogovor:
    #         self.ids["sporocila_box"].add_widget(Sporocilo)

        # self.ids["sporocila_rv"].data.clear()
        # self.ids["sporocila_rv"].refresh_from_data()

        # for Sporocilo in self.Pogovor:
        #     sporocilo = Sporocilo.to_dict()
        #     self.ids["sporocila_rv"].data.insert(0, sporocilo)
        #     self.ids["sporocila_rv"].refresh_from_data()

        # self.ids["sporocila_rv"].data.append(mehurcek)
        # print(self.ids["sporocila_rv"].opts)

    def poslji_sporocilo_gpt(self, sporocilo):
        api_sporocila = self.pogovor.pripravi_api_sporocila()
        api_odgovor = poslji_gpt_api(api_sporocila)
        sporocilo.odgovor_se_nalaga = False
        sporocilo.odgovor = api_odgovor
        # self.posodobi_sporocila()
        Clock.schedule_once(lambda x: self.posodobi_sporocila(), 0)

    def poslji_sporocilo(self):
        vnosno_polje = self.ids["vnosno_polje"]
        vnosno_sporocilo = vnosno_polje.text.strip()
        if vnosno_sporocilo:
            vnosno_polje.text = ""
            # chat = upravitelj_pogovorov.get_chat(self.name)
            # chat["messages"].append({"text": message_text, "user": "User"})
            # chat_input = chat["messages"][-1]
            # self.update_messages()
            # message_input.text = ""
            # self.process_gpt_response(chat_input)
            novo_sporocilo = Sporocilo(vprasanje=vnosno_sporocilo)
            self.pogovor.dodaj_sporocilo(novo_sporocilo)
            self.posodobi_sporocila()

            api_nit = threading.Thread(
                target=self.poslji_sporocilo_gpt, args=(novo_sporocilo,))
            api_nit.start()

    def preimenuj_dialog_potrdi(self, novo_ime_pogovora):
        novo_ime_pogovora = novo_ime_pogovora.strip()
        if novo_ime_pogovora:
            self.pogovor.spremeni_ime(novo_ime_pogovora)
            self.ids["pogovor_naslov"].title = self.pogovor.ime
            self.preimenuj_dialog.dismiss()

        # self.Pogovor.spremeni_ime(preimenujVnosnoPolje.text)

    def prikazi_dialog_preimenuj(self, *args, **kwargs):
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
        upravitelj_pogovorov.zbrisi_pogovor(self.pogovor.id)
        self.zbrisi_dialog.dismiss()
        self.zamenjaj_zalon_pogovori()

        # prikazi sporocilo - uspesno izbrisan pogovor (na zacetnem zaslonu)
        uZ = self.parent
        # print(uZ)
        zz = uZ.get_screen("zacetniZaslon")
        zz.prikazi_obvestilo(
            f'Pogovor "{self.pogovor.ime}" je bil uspešno izbrisan!')

        # novo_ime_pogovora = novo_ime_pogovora.strip()
        # if novo_ime_pogovora:
        #     self.Pogovor.spremeni_ime(novo_ime_pogovora)
        #     self.ids["pogovor_naslov"].title = self.Pogovor.ime
        #     self.preimenuj_dialog.dismiss()

    def prikazi_dialog_zbrisi(self, *args, **kwargs):
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

    def zamenjaj_zalon_pogovori(self, *args, **kwargs):
        uZ = self.parent
        uZ.zamenjaj_zaslon("zacetniZaslon")

    def on_enter(self):
        self.ids["pogovor_naslov"].title = self.pogovor.ime
        self.posodobi_sporocila()
        # self.appendMsg(False, 'zdravo')
        # for x in range(14):
        #     text = lorem.sentence()
        #     text1 = lorem.sentence()
        #     novo_sporocilo = Sporocilo(text, text1)
        #     # self.Pogovor.dodaj_sporocilo(novo_sporocilo)
        #     self.ids["sporocila_box"].add_widget(novo_sporocilo)

        # self.posodobi_sporocila()
        # print(dir(self.Pogovor))

        uZ = self.parent
        uZ.zamenjaj_smer_prehoda()


"""     def __init__(self, pn, **kwargs):
        super().__init__(**kwargs)
        self.name = pn
 """
