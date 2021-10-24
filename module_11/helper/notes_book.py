'''содержит методы по работе с таблицей notes'''
from .db_classes import Note


class NotesBook:
    '''содержит методы по работе с таблицей notes'''

    def __init__(self, session):
        self.session = session

    def all_notes(self):
        '''возвращает все заметки'''
        return self.session.query(Note).all()

    def add_note(self, text, hashtag, created_at):
        '''добавляет заметку в таблицу Notes'''
        self.session.add(
            Note(note_tags=hashtag, note_text=text, created_at=created_at))
        self.session.commit()

    def delete_note(self, note_id):
        ''' удаляет заметку из таблицы Notes, которая имеет note_tags=hashtag'''
        note_for_deleting = self.session.query(
            Note).filter_by(id=note_id).one()
        self.session.delete(note_for_deleting)
        self.session.commit()

    def find_note_for_editing(self, note_id):
        '''возвращает заметку для дальнейшего редактирования'''
        return self.session.query(Note).filter_by(id=note_id).one()

    def edit_note(self, note_id, new_text, new_hashtag):
        '''редактирует заметку из таблицы Notes, которая имеет note_tags=hashtag'''
        note_for_editing = self.session.query(Note).filter_by(id=note_id).one()
        note_for_editing.note_text = new_text
        note_for_editing.note_tags = new_hashtag
        self.session.commit()

    def find_notes(self, keyword):
        '''находит все заметки, которые содержат keyword в тексте или тегах заметки'''
        query1 = self.session.query(Note).filter(
            Note.note_tags.like(f"%{keyword}%"))
        query2 = self.session.query(Note).filter(
            Note.note_text.like(f"%{keyword}%"))
        return query1.union(query2).all()

    def sort_notes(self, search_type="1"):
        '''выводит список заметков в отсортированном виде
        1 - в алфавитном порядке
        2 - в обратном алфавитном порядке
        3 - от старых заметок к новым
        4 - от новых заметок к старым
        возвращает Note_list'''

        if search_type == "1":
            note_list = self.session.query(
                Note).order_by(Note.note_tags.asc()).all()
        elif search_type == "2":
            note_list = self.session.query(Note).order_by(
                Note.note_tags.desc()).all()
        elif search_type == "3":
            note_list = self.session.query(Note).order_by(Note.id.asc()).all()
        elif search_type == "4":
            note_list = self.session.query(Note).order_by(Note.id.desc()).all()
        return note_list
