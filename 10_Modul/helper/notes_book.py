from datetime import datetime
from pymongo import ASCENDING, DESCENDING


class NotesBook():

    def __init__(self, db):
        self.db = db
        self.db.notesbook

    def all_notes(self):
        # возвращает итератор по записям
        return self.db.notesbook.find()

    def add_note(self, text, hashtag):
        # добавляет заметку в таблицу Notes
        note = {"note_tags": hashtag,
                "note_text": text,
                "created_at": datetime.now()}
        self.db.notesbook.insert_one(note)

    def delete_note(self, hashtag):
        # удаляет заметку из таблицы Notes, которая имеет note_tags=hashtag
        self.db.notesbook.remove({"note_tags": hashtag})

    def get_note_text_for_editing(self, hashtag):
        # возвращает текст заметки с заданным тэгом
        note_for_editing = self.db.notesbook.find_one({'note_tags': hashtag})
        return note_for_editing['note_text']

    def edit_note(self, hashtag, new_text):
        # редактирует заметку из таблицы Notes, которая имеет note_tags=hashtag
        self.db.notesbook.update_one({'note_tags': hashtag}, {
            '$set': {'note_text': new_text}})

    def find_note(self,  keyword):
        # находит все заметки  из notesbook, в тэгах которых содержится keyword
        # возвращает note_list - список экземляра класса Note
        return self.db.notesbook.find(filter={'note_tags': {'$regex': keyword}})

    def print_notes(self, note_list):
        # где note_list - список экземляра класса Note

        result = ""

        # Печать шапки с названием столбцов
        result += f" {72*'_'} \n"
        result += '|             TAGS             |                NOTE                     |\n'
        result += f"|{71*'_'} |\n"
        # Печать заметок
        for note in note_list:
            lines = note['note_text'].split('\n')
            counter = 0
            for line in lines:
                if counter == 0:
                    result += f'|{note["note_tags"]:<30}| {line:<40}|\n'
                else:
                    result += f'|{" ":<30}| {line:<40}|\n'
                counter += 1
            result += f'|{30*"_"}|{41*"_"}|\n'
        print(result)

    def sort_notes(self, search_type="1"):
        # выводит список заметков в отсортированном виде
        # "1" - в алфавитном порядке
        # "2" - в обратном алфавитном порядке
        # "3" - от старых заметок к новым
        # "4" - от новых заметок к старым
        # возвращает Note_list
        if search_type == "1":
            note_list = self.db.notesbook.find().sort('note_tags', ASCENDING)
        elif search_type == "2":
            note_list = self.db.notesbook.find().sort('note_tags', DESCENDING)
        elif search_type == "3":
            note_list = self.db.notesbook.find().sort('created_at', ASCENDING)
        elif search_type == "4":
            note_list = self.db.notesbook.find().sort('created_at', DESCENDING)
        return note_list
