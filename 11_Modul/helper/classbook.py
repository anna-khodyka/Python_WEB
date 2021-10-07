import re
from datetime import datetime, timedelta, date
from sqlalchemy import extract
from sqlalchemy.sql.selectable import subquery

from .db_classes import Record, Phone


class AddressBook():
    def __init__(self, session):
        self.session = session

    def add_record(self, name, birthday=None, address=None, email=None, tags=None, phones=None):

        record = Record(name=name, birthday=birthday,
                        address=address, email=email, tags=tags)

        for phone in phones:
            record.phones.append(Phone(phone_value=phone))

        self.session.add(record)
        self.session.commit()
        print('This contact adds to DB:')
        print(record)

    def remove_record(self, id):
        # удаляет record с указанным id
        record = self.session.query(Record).filter_by(id=id).one()
        self.session.delete(record)
        self.session.commit()
        return str(record)

    def edit_name(self, edited_id, new_field_value):
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.name = new_field_value
        self.session.commit()
        return str(record)

    def edit_phone(self, edited_id, new_field_value):
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.phones.append(Phone(phone_value=new_field_value))
        self.session.commit()
        return str(record)

    def edit_birthday(self, edited_id, new_field_value):
        new_field_value = datetime.strptime(new_field_value, "%d.%m.%Y").date()
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.birthday = new_field_value
        self.session.commit()
        return str(record)

    def edit_address(self, edited_id, new_field_value):
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.address = new_field_value
        self.session.commit()
        return str(record)

    def edit_email(self, edited_id, new_field_value):
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.email = new_field_value
        self.session.commit()
        return str(record)

    def edit_tags(self, edited_id, new_field_value):
        record = self.session.query(Record).filter_by(id=edited_id).one()
        record.tags = new_field_value
        self.session.commit()
        return str(record)

    def return_all_records(self):
        # возвращает список объектов Record
        return self.session.query(Record).all()

    def find_value(self, keyword):
        # возвращает список объектов Record
        q1 = self.session.query(Record).filter(
            Record.name.like(f'%{keyword}%'))
        q2 = self.session.query(Record).filter(
            Record.tags.like(f'%{keyword}%'))
        q3 = self.session.query(Record).filter(
            Record.address.like(f'%{keyword}%'))
        records_list = q1.union(q2, q3).all()
        return records_list

    def iterator(self, records_list, n):
        # возвращает текстовое представление объекта для консольного интерфейса
        counter = 0
        result = ""
        for record in records_list:
            # записи строки с описанием 1 контакта
            result += str(record)
            counter += 1
            if counter == n:
                result = result.rstrip("\n")
                yield result
                result = ""
                counter = 0
        if result:
            result = result.rstrip("\n")
            yield result

    def find_persons_with_birthday_in_n_days(self, n):
        # ищет людей с др в data
        # возвращает список объектов Record
        if n >= 365:
            n = n % 365
        bdate = datetime.now().date()+timedelta(days=n)
        b_day = bdate.day
        b_month = bdate.month
        # поиск
        birthday_book = self.session.query(
            Record).filter(extract('month', Record.birthday) == b_month, extract('day', Record.birthday) == b_day).all()
        return bdate, birthday_book

    def find_persons_with_birthday_during_n_days(self, n):
        birthday_book = []
        # current_date = datetime.now().date()
        # limit_date = current_date+timedelta(days=n)
        # print(f'Current date is {current_date}, limit date is {limit_date}')

        # birthday_book = self.session.query(
        #     Record).filter(Record.birth_this_year >= current_date, Record.birth_this_year <= limit_date).all()
        return birthday_book

    def find_persons_birthday(self, name):
        # возвращает список кортежей (имя, дней до ДР)
        records_list = self.find_value(name)
        result = []
        for record in records_list:
            result.append(
                (record.name, AddressBook.days_to_birthday(record.birthday)))
        return result

    @ staticmethod
    def days_to_birthday(bday):
        today_d = datetime.now().date()
        if bday == None:
            return None
        bday = bday.replace(year=today_d.year)
        if today_d > bday:
            bday = date(today_d.year+1, bday.month, bday.day)
            days_left = (bday-today_d)
        else:
            days_left = (bday-today_d)
        return days_left.days

    def validate_phone(self, phone):
        return re.fullmatch('[+]?[0-9]{3,12}', phone)

    def validate_address(self, address):
        return len(address) > 1 and len(address) <= 30

    def validate_tags(self, tags):
        return len(tags) > 1 and len(tags) <= 15

    def validate_email_format(self, email):
        return re.match('([a-zA-Z][a-zA-Z0-9\._!#$%^*=\-]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})', email)

    def validate_email_duration(self, email):
        return (len(email) > 1 and len(email) <= 30)

    def validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y").date()
            return True
        except:
            return False
