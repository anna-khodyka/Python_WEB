from .notes_book import NotesBook
from .classbook import AddressBook


class Model:
    def __init__(self, session):
        self.session = session
        self.book = AddressBook(self.session)
        self.notes_book = NotesBook(self.session)
