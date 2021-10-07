from .db_classes import Note


class NotesBook():

    def __init__(self, session):
        self.session = session

    def all_notes(self):
        return self.session.query(Note).all()

    def add_note(self, text, hashtag):
        # добавляет заметку в таблицу Notes
        self.session.add(Note(note_tags=hashtag, note_text=text))
        self.session.commit()

    def delete_note(self, hashtag):
        # удаляет заметку из таблицы Notes, которая имеет note_tags=hashtag
        note_for_deleting = self.session.query(
            Note).filter_by(note_tags=hashtag).first()
        self.session.delete(note_for_deleting)
        self.session.commit()

    def find_note_for_editing(self, hashtag):
        # возвращает текст заметки с заданным тэгом
        note_for_editing = self.session.query(
            Note).filter_by(note_tags=hashtag).one()
        return note_for_editing.note_text

    def edit_note(self, hashtag, new_text):
        # редактирует заметку из таблицы Notes, которая имеет note_tags=hashtag
        note_for_editing = self.session.query(
            Note).filter_by(note_tags=hashtag).one()
        note_for_editing.note_text = new_text
        self.session.commit()

    def find_note(self,  keyword):
        # находит все заметки  из таблицы Notes, в тэгах которых содержится keyword
        # возвращает note_list - список экземляра класса Note

        note_list = self.session.query(Note).filter_by(note_tags=keyword).all()
        return note_list

    def print_notes(self, note_list):
        # где note_list - список экземляра класса Note

        result = ""

        # Печать шапки с названием столбцов
        result += f" {72*'_'} \n"
        result += '|             TAGS             |                NOTE                     |\n'
        result += f"|{71*'_'} |\n"
        # Печать заметок
        for note in note_list:
            lines = note.note_text.split('\n')
            counter = 0
            for line in lines:
                if counter == 0:
                    result += f'|{note.note_tags:<30}| {line:<40}|\n'
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
            note_list = self.session.query(Note).order_by(
                Note.note_tags.asc()).all()
        elif search_type == "2":
            note_list = self.session.query(Note).order_by(
                Note.note_tags.desc()).all()
        elif search_type == "3":
            note_list = self.session.query(Note).order_by(
                Note.id.asc()).all()
        elif search_type == "4":
            note_list = self.session.query(Note).order_by(
                Note.id.desc()).all()
        return note_list
