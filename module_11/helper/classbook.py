"""Classbook module
В данном модуле описан class AddressBook для работы с таблицей Record"""
import re
from datetime import datetime, date

from .db_classes import Record, Phone


class AddressBook:
    """класс для работы с таблицей Record"""

    def __init__(self, session):
        self.session = session

    def add_record(
        self, name, birthday=None, address=None, email=None, tags=None, phones=None
    ):
        """добавляет запись"""
        record = Record(
            name=name, birthday=birthday, address=address, email=email, tags=tags
        )
        # добавить проверку на phones <> None
        for phone in phones:
            record.phones.append(Phone(phone_value=phone))

        self.session.add(record)
        self.session.commit()
        print("This contact adds to DB:")
        print(record)

    def remove_record(self, record_id):
        """удаляет record с указанным id"""
        record = self.session.query(Record).filter_by(id=record_id).one()
        self.session.delete(record)
        self.session.commit()
        return str(record)

    def edit_record(
        self,
        edited_id,
        updated_name,
        updated_birthday,
        updated_address,
        updated_email,
        updated_tags,
        updated_phone,
    ):
        """редактирует record"""
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.name = updated_name
        record.phones = []
        record.phones.append(Phone(phone_value=updated_phone))
        record.birthday = updated_birthday
        record.address = updated_address
        record.email = updated_email
        record.tags = updated_tags
        self.session.commit()
        return str(record)

    def return_all_records(self):
        """возвращает список объектов Record"""
        return self.session.query(Record).all()

    def find_record(self, edited_id):
        """находит один record"""
        return self.session.query(Record).filter_by(id=edited_id).one()

    def find_value(self, keyword):
        """возвращает список объектов Record, которые содержат keyword"""
        query1 = self.session.query(Record).filter(Record.name.like(f"%{keyword}%"))
        query2 = self.session.query(Record).filter(Record.tags.like(f"%{keyword}%"))
        query3 = self.session.query(Record).filter(Record.address.like(f"%{keyword}%"))
        records_list = query1.union(query2, query3).all()
        return records_list

    def sort(self, sort_type):
        """сортирует records"""
        if sort_type == "1":
            records_list = self.session.query(Record).order_by(Record.name.asc()).all()
        elif sort_type == "2":
            records_list = self.session.query(Record).order_by(Record.name.desc()).all()
        elif sort_type == "3":
            records_list = self.session.query(Record).order_by(Record.id.asc()).all()
        elif sort_type == "4":
            records_list = self.session.query(Record).order_by(Record.id.desc()).all()
        return records_list

    @staticmethod
    def validate_phone(phone):
        """валидирует телефон"""
        return re.fullmatch("[+]?[0-9]{3,12}", phone)

    @staticmethod
    def validate_address(address):
        """валидирует адресс"""
        return len(address) > 1 and len(address) <= 30

    @staticmethod
    def validate_tags(tags):
        """валидирует тєги"""
        return len(tags) > 1 and len(tags) <= 15

    @staticmethod
    def validate_email_format(email):
        """валидирует ємейл"""
        return re.match(
            r"([a-zA-Z][a-zA-Z0-9\._!#$%^*=\-]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})", email
        )

    # @staticmethod
    # def validate_email_duration(email):
    #     '''валидирует длину ємейла'''
    #     return len(email) > 1 and len(email) <= 30

    @staticmethod
    def validate_birthday(birthday):
        """валидирует дату рождения"""
        try:
            datetime.strptime(birthday, r"%d.%m.%Y").date()
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_birthday2(birthday):
        """валидирует дату рождения"""
        try:
            datetime.strptime(birthday, "%Y-%m-%d").date()
            return True
        except ValueError:
            return False
