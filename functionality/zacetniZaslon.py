from kivy.clock import Clock
from functools import partial


from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.list import OneLineIconListItem

from .pogovor import upravitelj_pogovorov
# from .upravljalecZaslonov import nalozi_pogovor
# from .pogovor import nalozi_pogovore
# from .pogovor import UpraviteljPogovorov


class ZacetniZaslon(MDScreen):
    # pogovoriObstajajo = BooleanProperty(False)

    # def __init__(self, **kwargs):
    #     super(ZacetniZaslon, self).__init__(**kwargs)
    #     Clock.schedule_once(self.nalozi_pogovore, 0.5)

    # self.__ = vprasanje
    # self.odgovor = odgovor
    # self.odgovor_se_nalaga = odgovor_se_nalaga
    # _casovni_zig = time.strftime("%Y.%m.%d - %H:%M", time.localtime())
    # self.casovni_zig = _casovni_zig

    # # ce vprasanje se nima odgovora, prikazi nalaganje (nalagalne pike)
    # Clock.schedule_once(self.animacija_odgovor, 0.5)
    # # print(self.height)
    # self.height = self.children[0]True.texture_size[1] + self.children[1].texture_size[1]

    def zacni_pogovor(self, *args, **kwargs):
        nov_pogovor_id = upravitelj_pogovorov.ustvari_nov_pogovor()
        uZ = self.parent
        pZ = uZ.get_screen("pogovorZaslon")
        pZ.spremeni_pogovor(nov_pogovor_id)
        uZ.zamenjaj_zaslon("pogovorZaslon")

    def prikazi_obvestilo(self, obvestilo_text):
        # # Create a BoxLayout to hold the centered label
        toast(obvestilo_text, duration=5)
        # centered_label = MDBoxLayout(
        #     orientation="vertical", size_hint_x=1, height="46dp")
        # centered_label.add_widget(MDLabel(
        #     text=f"[color=#ddbb34]{obvestilo_text}[/color]",
        #     markup=True, halign="center"))
        # # Create the Snackbar with the centered label
        # self.snackbar = Snackbar(
        #     snackbar_y="25dp",
        #     size_hint_x=0.7,nalozi_pogovore
        #     pos_hint={'center_x': 0.5},
        #     opacity=0.75
        # )

        # # Add the centered label to the Snackbar
        # self.snackbar.add_widget(centered_label)
        # Create a BoxLayout to hold the centered label

        # Set the label's width to match the Snackbar width

        # Create the Snackbar with the centered label
        # self.snackbar = Snackbar(
        #     snackbar_y="25dp",
        #     size_hint_x=0.7,
        #     pos_hint={'center_x': 0.5},
        #     opacity=0.75
        # )

        # centered_label = MDBoxLayout(
        #     orientation="vertical",
        #     size_hint_x=None,
        #     height="46dp",
        # )
        # centered_label.width = self.snackbar.width

        # # Add the notification text to the label
        # centered_label.add_widget(
        #     MDLabel(
        #         text=f"[color=#ddbb34]{obvestilo_text}[/color]",
        #         markup=True,
        #         halign="left",
        #     )
        # )

        # Add the centered label to the Snackbar
        # self.snackbar.add_widget(centered_label)

        # # self.snackbar = Snackbar(
        #     text=f'[color=#ddbb34]{obvestilo_text}[/color]',
        #     font_size="18sp",
        #     # snackbar_y="50dp",
        #     # snackbar_x="100dp",
        #     snackbar_y="25dp",
        #     size_hint_x=0.7,
        #     # snackbar_animation_dir="Top",
        #     pos_hint={'center_x': 0.5},
        #     # bg_color=(0, 255, 0),
        #     # md_bg_color=(158, 179, 241),
        #     opacity=0.75
        # )
        # self.snackbar.open()

    def prikazi_uvodno_sporocilo(self, je_vidno):
        prikazi_sporocilo = int(je_vidno)
        self.ids.uvodno_sporocilo.opacity = prikazi_sporocilo
        self.ids.uvodno_sporocilo.size_hint = (
            prikazi_sporocilo, prikazi_sporocilo)

    def prikazi_pogovor(self, pogovor_id, *args, **kwargs):
        uZ = self.parent
        pZ = uZ.get_screen("pogovorZaslon")
        pZ.spremeni_pogovor(pogovor_id)
        uZ.zamenjaj_zaslon("pogovorZaslon")

    def prikazi_pogovore(self, pogovori, *args, **kwargs):
        self.ids.pogovori_list.clear_widgets()
        for pogovor in pogovori:
            on_release_fun = partial(self.prikazi_pogovor, pogovor.id)
            self.ids.pogovori_list.add_widget(OneLineIconListItem(
                IconLeftWidget(icon="forum-outline"),
                on_release=on_release_fun,
                text=f'{pogovor.ime}'))
        # print(self.ids)

    def nalozi_pogovore(self, *args, **kwargs):
        # print("calles")
        self.pogovori = upravitelj_pogovorov.dobi_pogovore()
        self.prikazi_pogovore(pogovori=self.pogovori)

        # self.pogovoriObstajajo = True
        if len(self.pogovori) > 0:
            self.prikazi_uvodno_sporocilo(False)
        else:
            self.prikazi_uvodno_sporocilo(True)
            # selfupravitelj_pogovorov.pirkazi_

        # print(self.pogovoriObstajajo)
        # else:
            # self.pogovoriObstajajo = True
            # print("hesss")
            # print(len(self.pogovori))
            # print(self.ids)

    def on_enter(self, *args, **kwargs):
        Clock.schedule_once(self.nalozi_pogovore, 0.25)

        # self.pogovoriNeObstajajo = MDLabel(
        #     height=self.height, halign="center",
        #     text="Ni se pogovorov, ustvari novega?"
        # )
        # .add_widget(self.pogovoriNeObstajajo)

        # self.pogovori = upravitelj_pogovorov.dobi_pogovore()

        # self.ids.pogovoriView.remove_widget(self.pogovoriNeObstajajo)
        # self.ids.pogovori_obstajajo.height = "0dp"
        # self.ids.pogovori_obstajajo.opacity = 0
        # self.ids.pogovori_obstajajo.opacity = self.height
        # self.pogovoriObstajajo = True
        # else:
        #   Clock.schedule_once(self., 0.5)
        # print("Entered BaseScreen")
        # MDLabel:
        #     height: dp(0) if not root.pogovoriObstajajo else self.height
        #     opacity: 0 if not root.pogovoriObstajajo else 1
        #     halign: "center"
        #     text: "Ni se pogovorov, ustvari novega?"

        # upravitelj_pogovorov
        # Clock.schedule_once(self.zacni_pogovor, 0.5)
        uZ = self.parent
        uZ.zamenjaj_smer_prehoda()
