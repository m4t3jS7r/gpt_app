from kivymd.uix.screenmanager import MDScreenManager


class UpravljalecZaslonov(MDScreenManager):
    def zamenjaj_smer_prehoda(self):
        smer_prehoda_je_desna = self.transition.direction == "right"
        obratna_smer = "left" if smer_prehoda_je_desna else "right"
        self.transition.direction = obratna_smer

    def zamenjaj_zaslon(self, zaslonIme):
        self.current = zaslonIme
        # Clock.schedule_once(self.zamenjaj_smer_prehoda, 0.)
        # self.zamenjaj_smer_prehoda()
