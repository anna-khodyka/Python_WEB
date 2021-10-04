from pymongo import MongoClient
from notes_book import NotesBook
from classbook import AddressBook

client = MongoClient(
    "mongodb+srv://anya:0978440021@hw10.qxnnu.mongodb.net/hw10?retryWrites=true&w=majority"
)

db = client.helper


class Model:
    def __init__(self):
        self.db = db
        self.book = AddressBook(self.db)
        self.notes_book = NotesBook(self.db)
