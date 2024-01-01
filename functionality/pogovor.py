import atexit
import json
import time

from .sporocilo import Sporocilo
# class Pogovor:
#     def __enter__(self):
#         self.chats = shelve.open(self.storage_file)
#         return self

#     def create_chat(self, chat_name):
#         if chat_name not in self.chats:
#             self.chats[chat_name] = {"messages": []}
#             return True  # Chat created successfully
#         else:
#             return False  # Chat with the same name already exists

#     def get_chat(self, chat_name):
#         return self.chats.get(chat_name, {"messages": []})

#     def send_message(self, chat_name, message):
#         chat = self.get_chat(chat_name)
#         if chat:
#             chat["messages"].append({"text": message, "user": "User"})

#     def preimenuj_pogovor(self, idPogovora, imePogovora):
#         # self.pogovori.append(
#         #     {"id": id_pogovora,
#         #      "ime": f"Pogovor {id_pogovora}",
#         #      "pogovor": Pogovor()})
#         pogovor = self._najdi_pogovor(idPogovora)
#         pogovor.ime = imePogovora


"""
# Example usage with the context manager
with ChatManager() as upravitelj_pogovorov:
    # Create a new chat
    if upravitelj_pogovorov.create_chat("General"):
        print("Chat 'General' created successfully!")
    else:
        print("Chat 'General' already exists!")

    # Get chat messages
    general_chat = upravitelj_pogovorov.get_chat("General")
    print("Messages in 'General' chat:", general_chat["messages"])
 """
# The context manager will automatically close the storage when exiting the 'with' block


class Pogovor:
    def __init__(self):
        self.id = int(time.time())
        self.ime = f'Pogovor #{str(self.id%1000)}'
        self.sporocila = []

    def __iter__(self):
        for sporocilo in reversed(self.sporocila):
            yield sporocilo

    def pripravi_api_sporocila(self):
        sporocila = []
        for sporocilo in self.sporocila:
            sporocila.extend(sporocilo.to_api_list())
        return sporocila

    def to_dict(self):
        return {'id': self.id, 'ime': self.ime,
                'sporocila': [sporocilo.to_dict() for sporocilo in self.sporocila]}

    @classmethod
    def from_dict(cls, dict):
        pogovor = cls()
        pogovor.id = dict['id']
        pogovor.ime = dict['ime']
        pogovor.sporocila = [Sporocilo.from_dict(sporocilo)
                             for sporocilo in dict['sporocila']]
        return pogovor
    # Add these methods for pickling support
    # def __getstate__(self):
    #     return self.__dict__

    # def __setstate__(self, state):
    #     self.__dict__ = state

    def preveri_nov_pogovor(self):
        return not len(self.sporocila)

    def dodaj_sporocilo(self, sporocilo):
        self.sporocila.append(sporocilo)

    def zbrisi_sporocilo(self, idSporocila):
        Sporocilo = self._najdi_sporocilo(idSporocila)
        self.sporocila.remove(Sporocilo)

    def _najdi_sporocilo(self, idSporocila):
        for Sporocilo in self.sporocila:
            if Sporocilo.id == idSporocila:
                return Sporocilo

    def spremeni_ime(self, novo_ime):
        self.ime = novo_ime


# class ChatManager:
#     def __init__(self, filename):
#         self.filename = filename
#         self.chats = self._load_chats()

#     def _load_chats(self):
#         with shelve.open(self.filename) as db:
#             return [self._create_chat_from_data(chat_id, chat_data) for chat_id, chat_data in db.items()]

#     def _create_chat_from_data(self, chat_id, chat_data):
#         chat = Chat(chat_id)
#         chat.messages = chat_data
#         return chat

#     def _save_chats(self):
#         with shelve.open(self.filename) as db:
#             for chat in self.chats:
#                 db[chat.name] = chat.messages

#     def create_chat(self, name):
#         chat = Chat(name)
#         self.chats.append(chat)
#         self._save_chats()
#         return chat

#     def remove_chat(self, name):
#         for chat in self.chats:
#             if chat.name == name:
#                 self.chats.remove(chat)
#                 break
#         self._save_chats()

#     def list_chats(self):
#         print("List of chats:")
#         for index, chat in enumerate(self.chats, 1):
#             print(f"{index}. {chat.name}")

#     def get_chat(self, name):
#         for chat in self.chats:
#             if chat.name == name:
#                 return chat
#         return None

#     def add_message_to_chat(self, name, message):
#         chat = self.get_chat(name)
#         if chat:
#             chat.add_message(message)
#             self._save_chats()
#         return chat


class UpraviteljPogovorov:
    def __init__(self, *args, **kwargs):
        self.pogovori = []
        self.nalozi_iz_db()
        atexit.register(self.shrani_v_db)
#         self.filename = filename
#         self.chats = self._load_chats()

    def shrani_v_db(self):
        if self.pogovori:
            with open('pogovori.json', 'w') as db:
                json.dump(self.to_dict(), db)
                # dill.dump(self.pogovori, db)

    def nalozi_iz_db(self):
        try:
            with open('pogovori.json', 'r') as db:
                dict = json.load(db)
                self.from_dict(dict)
        except FileNotFoundError:
            print("db datoteka se ne obstaja")

    def to_dict(self):
        return {'pogovori': [pogovor.to_dict() for pogovor in self.pogovori]}

    def from_dict(self, dict):
        self.pogovori = [Pogovor.from_dict(pogovor)
                         for pogovor in dict['pogovori']]

    def dobi_pogovore(self):
        # print(self.pogovori)
        return self.pogovori
    # def _ustvari_pogovor(self, idPogovora, Pogovor):
    #     try:
    #         with shelve.open(self.db_datoteka) as db:
    #             serialized_data = db[str(idPogovora)]
    #             return pickle.loads(serialized_data)
    #     except KeyError:
    #         return None

    def ustvari_nov_pogovor(self):
        nov_pogovor = Pogovor()
        self.pogovori.append(nov_pogovor)
        return nov_pogovor.id

    def dobi_pogovor(self, pogovor_id):
        for pogovor in self.pogovori:
            if pogovor.id == pogovor_id:
                return pogovor

    def zbrisi_pogovor(self, pogovor_id):
        pogovor = self.dobi_pogovor(pogovor_id)
        self.pogovori.remove(pogovor)
        # self.pogovori.remove(Pogovor)
    # def dobi_pogovor(self, pogovor):

    #     if self.pogovori[idPogovora]:
    #         return self.pogovori[idPogovora]
    #     return None


upravitelj_pogovorov = UpraviteljPogovorov()
