from .db_classes import Note


class NotesBook:
    def __init__(self, session):
        self.session = session

    def all_notes(self):
        return self.session.query(Note).all()

    def add_note(self, text, hashtag, created_at):
        # добавляет заметку в таблицу Notes
        self.session.add(Note(note_tags=hashtag, note_text=text, created_at=created_at))
        self.session.commit()

    def delete_note(self, id):
        # удаляет заметку из таблицы Notes, которая имеет note_tags=hashtag
        note_for_deleting = self.session.query(Note).filter_by(id=id).one()
        self.session.delete(note_for_deleting)
        self.session.commit()

    def find_note_for_editing(self, id):
        # возвращает заметку для дальнейшего редактирования
        return self.session.query(Note).filter_by(id=id).one()

    def edit_note(self, id, new_text, new_hashtag):
        # редактирует заметку из таблицы Notes, которая имеет note_tags=hashtag
        note_for_editing = self.session.query(Note).filter_by(id=id).one()
        note_for_editing.note_text = new_text
        note_for_editing.note_tags = new_hashtag
        self.session.commit()

    def find_notes(self, keyword):
        # находит все заметки, которые содержат keyword в тексте или тегах заметки
        q1 = self.session.query(Note).filter(Note.note_tags.like(f"%{keyword}%"))
        q2 = self.session.query(Note).filter(Note.note_text.like(f"%{keyword}%"))
        return q1.union(q2).all()

    def print_notes(self, note_list):
        # где note_list - список экземляра класса Note

        result = ""

        # Печать шапки с названием столбцов
        result += f" {72*'_'} \n"
        result += "|             TAGS             |                NOTE                     |\n"
        result += f"|{71*'_'} |\n"
        # Печать заметок
        for note in note_list:
            lines = note.note_text.split("\n")
            counter = 0
            for line in lines:
                if counter == 0:
                    result += f"|{note.note_tags:<30}| {line:<40}|\n"
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
            note_list = self.session.query(Note).order_by(Note.note_tags.asc()).all()
        elif search_type == "2":
            note_list = self.session.query(Note).order_by(Note.note_tags.desc()).all()
        elif search_type == "3":
            note_list = self.session.query(Note).order_by(Note.id.asc()).all()
        elif search_type == "4":
            note_list = self.session.query(Note).order_by(Note.id.desc()).all()
        return note_list
