import atexit
import json
import time

# uvozi Sporocilo razred iz sporocilo.py datoteke
from .sporocilo import Sporocilo


class Pogovor:
    """
    implementacija razreda za pogovor (funckionalnost)
    """

    def __init__(self):
        """
        ustvari nov objekt tipa Pogovor
        """
        # koda se zažene, ko se ustvari nov Pogovor objekt
        self.id = int(time.time())
        self.ime = f'Pogovor #{str(self.id%1000)}'
        self.sporocila = []  # seznam sporocil pogovora

    def __iter__(self):
        """
        omogoči for zanko za Pogovor objekte (vrstni red sporocil je obrnjen)
        """
        for sporocilo in reversed(self.sporocila):
            yield sporocilo

    def pripravi_api_sporocila(self):
        """
        pripravi seznam sporocil za OpenAI API (zgodovina pogovora)
        """
        sporocila = []
        for sporocilo in self.sporocila:
            sporocila.extend(sporocilo.to_api_list())
        return sporocila

    def to_dict(self):
        """
        pretvori objekt tipa Pogovor v knjizno obliko
        """
        # uporabljeno pri shranjevanju
        return {'id': self.id, 'ime': self.ime,
                'sporocila': [sporocilo.to_dict() for sporocilo in self.sporocila]}

    @classmethod
    def from_dict(cls, dict):
        """
        ustvari in vrne objekt tipa Pogovor iz knjizne oblike 

        Parametri:
        - dict (dict): knjizna oblika Pogovor objekta
        """
        # uporabljeno za nalaganje (obstojecih) pogovorov
        pogovor = cls()
        pogovor.id = dict['id']
        pogovor.ime = dict['ime']
        pogovor.sporocila = [Sporocilo.from_dict(sporocilo)
                             for sporocilo in dict['sporocila']]
        return pogovor

    def preveri_nov_pogovor(self):
        """
        vrne True, ko pogovor nima sporocil
        """
        return not len(self.sporocila)

    def dodaj_sporocilo(self, sporocilo):
        """
        dodaj sporocilo na seznam sporcil v Pogovor objektu

        Parametri:
        - sporocilo (Sporocilo): sporocilo za dodajanje
        """
        self.sporocila.append(sporocilo)

    def spremeni_ime(self, novo_ime):
        """
        spremeni ime Pogovor objekta

        Parametri:
        - novo_ime (str): novo ime
        """
        # spremeni ime Pogovor objekta
        self.ime = novo_ime


class UpraviteljPogovorov:
    """
    implementacija razreda za UpraviteljPogovorov (funckionalnost)
    """

    def __init__(self, *args, **kwargs):
        """
        ustvari nov ojekt tipa UpraviteljPogovorov
        """
        # koda se zažene, ko je ustvarjen objekt UpraviteljPogovorov
        self.pogovori = []
        self.nalozi_iz_db()
        # ob izhodu se zažene metoda shrani_v_db
        atexit.register(self.shrani_v_db)

    def shrani_v_db(self):
        """
        shrani pogovore v JSON datoteko
        """
        if self.pogovori:
            with open('pogovori.json', 'w') as db:
                json.dump(self.to_dict(), db)

    def nalozi_iz_db(self):
        """
        nalozi pogovore iz .json datoteke
        """
        try:
            with open('pogovori.json', 'r') as db:
                dict = json.load(db)
                self.from_dict(dict)
        except FileNotFoundError:
            print("db datoteka se ne obstaja")

    def to_dict(self):
        """
        pretvori pogovore v knjizno okliko za shranjevanje
        """
        return {'pogovori': [pogovor.to_dict() for pogovor in self.pogovori]}

    def from_dict(self, dict):
        """
        ustvari UpraviteljPogovorov objekt iz obstojece knjiznice pogovorov

        Parametri:
        - dict (dict): knjizna oblika pogovorov
        """
        self.pogovori = [Pogovor.from_dict(pogovor)
                         for pogovor in dict['pogovori']]

    def dobi_pogovore(self):
        """
        vrne seznam vseh obstojecih pogovorov
        """
        return self.pogovori

    def ustvari_nov_pogovor(self):
        """
        ustvari nov objekt tipa Pogovor in ga dodaj na seznam pogovori
        metoda vrne id novega pogovora
        """
        nov_pogovor = Pogovor()
        self.pogovori.append(nov_pogovor)
        return nov_pogovor.id

    def dobi_pogovor(self, pogovor_id):
        """
        vrne objekt tipa Pogovor glede na pogovor_id
        """
        for pogovor in self.pogovori:
            if pogovor.id == pogovor_id:
                return pogovor

    def zbrisi_pogovor(self, pogovor_id):
        """
        zbrise objekt tipa Pogovor s seznama pogovori glede na pogovor_id
        """
        pogovor = self.dobi_pogovor(pogovor_id)
        self.pogovori.remove(pogovor)


# ustvari objekt razreda UpraviteljPogovorov
upravitelj_pogovorov = UpraviteljPogovorov()
