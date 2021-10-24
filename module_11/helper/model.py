'''создает класс Model() и подключает БД и методы по работе с ней'''
from .notes_book import NotesBook
from .classbook import AddressBook


class Model:
    '''обеспечивает подключение к sqlite-БД через session и методы по работе с ней'''

    def __init__(self, session):
        self.session = session
        self.book = AddressBook(self.session)
        self.notes_book = NotesBook(self.session)
