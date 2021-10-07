from .notes_book import NotesBook
from .classbook import AddressBook
from .db_classes import session


class Model:
    def __init__(self):
        self.session = session
        self.book = AddressBook(self.session)
        self.notes_book = NotesBook(self.session)
