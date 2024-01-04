from kivymd.uix.screenmanager import MDScreenManager


class UpravljalecZaslonov(MDScreenManager):
    def zamenjaj_smer_prehoda(self):
        """
        zamenja smer prehoda med desno in levo smerjo
        """
        smer_prehoda_je_desna = self.transition.direction == "right"
        obratna_smer = "left" if smer_prehoda_je_desna else "right"
        self.transition.direction = obratna_smer

    def zamenjaj_zaslon(self, zaslonIme):
        """
        spremeni trenutno prikazan zaslon

        Parametri:
        - zaslonIme (str): ime zaslona za prikaz
        """

        self.current = zaslonIme
