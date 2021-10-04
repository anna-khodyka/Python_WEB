import re
from datetime import datetime, timedelta, date


class AddressBook():
    def __init__(self, db):
        self.db = db
        self.db.book

    def add_record(self, name, birthday=None, address=None, email=None, tags=None, phones=None):
        record = {'name': name}
        if birthday:
            record['birthday'] = birthday
        if address:
            record['address'] = address
        if email:
            record['email'] = email
        if tags:
            record['tags'] = tags
        if phones:
            record['phones'] = phones
        # print(f'Получился вот такой record: {record}')
        self.db.book.insert_one(record)
        print('This contact adds to DB:')
        print(record)

    def remove_record(self, name):
        # удаляет record с указанным id
        self.db.book.remove({"name": name})

    def edit_name(self, edited_name, new_field_value):
        self.db.book.update_one({'name': edited_name}, {
            '$set': {'name': new_field_value}})


    def edit_phone(self, edited_name, new_field_value):
        self.db.book.update_one({'name': edited_name}, {
            '$set': {'phones': new_field_value}})

    def edit_birthday(self, edited_name, new_field_value):
        self.db.book.update_one({'name': edited_name}, {
            '$set': {'birthday': new_field_value}})

    def edit_address(self, edited_name, new_field_value):
        self.db.book.update_one({'name': edited_name}, {
            '$set': {'address': new_field_value}})

    def edit_email(self, edited_name, new_field_value):
        self.db.book.update_one({'name': edited_name}, {
            '$set': {'email': new_field_value}})

    def edit_tags(self, edited_name, new_field_value):
        self.db.book.update_one({'name': edited_name}, {
            '$set': {'tags': new_field_value}})

    def return_all_records(self):
        # возвращает список объектов Record
        return self.db.book.find()

    def find_value(self, keyword):
        # возвращает список объектов Record
        return self.db.book.find(filter={'$or': [{'name': {'$regex': keyword}}, {'email': {'$regex': keyword}}, {'phones': {'$regex': keyword}}, {'tags': {'$regex': keyword}}]})

    def iterator(self, records_list, n=-1):
        # возвращает текстовое представление объекта для консольного интерфейса
        pass
        counter = 0
        result = ""
        for record in records_list:
            # записи строки с описанием 1 контакта
            result += self.record_to_str(record)
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
        pass
        # if n >= 365:
        #     n = n % 365
        # bdate = datetime.now().date()+timedelta(days=n)
        # b_day = bdate.day
        # b_month = bdate.month
        # # поиск
        # birthday_book = self.session.query(
        #     Record).filter(extract('month', Record.birthday) == b_month, extract('day', Record.birthday) == b_day).all()
        # return bdate, birthday_book

    def find_persons_with_birthday_during_n_days(self, n):
        pass
        # birthday_book = []
        # # current_date = datetime.now().date()
        # # limit_date = current_date+timedelta(days=n)
        # # print(f'Current date is {current_date}, limit date is {limit_date}')

        # # birthday_book = self.session.query(
        # #     Record).filter(Record.birth_this_year >= current_date, Record.birth_this_year <= limit_date).all()
        # return birthday_book

    def find_persons_birthday(self, name):
        # возвращает список кортежей (имя, дней до ДР)
        pass
        # records_list = self.find_value(name)
        # result = []
        # for record in records_list:
        #     result.append(
        #         (record.name, AddressBook.days_to_birthday(record.birthday)))
        # return result

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

    def record_to_str(self, record):
        pass
        result = ""
        result += f'| {record["name"] if record["name"] else " ":<25}| { record["phones"][0] if record.get("phones") else " ":<15} | {str(record["birthday"]) if record.get("birthday") else " ":<11}|{record["address"] if record.get("address") else " ":<30}|  {record["email"] if record.get("email") else " ":<30}| {record["tags"] if record.get("tags") else " ":<15}|\n'
        if record.get("phones") and len(record["phones"]) > 1:
            for elem in record["phones"][1:]:
                result += f'|                          | {elem.phone_value: <15} |            |                              |                                |                | \n'
        result += " "
        result += f"{138*'_'}\n"
        return result
