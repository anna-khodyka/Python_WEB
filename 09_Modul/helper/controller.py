import pathlib
import pickle
import json
import re
import os
from datetime import datetime


from classbook import *
from model import *
from notes_book import *

from db_classes import *
from clean import *
from error_handler import error_handler

from view import *

YES_DECISION = {'y', 'yes', 'нуі', 'н', 'да', 'д'}

NO_DECISION = {'n', 'not', 'no', 'нет', 'тщ', 'тще', 'т'}

EXIT_DECISION = {'exit', 'учше', 'esc', 'close'}


AUTHORIZATION_COMMANDS = {('exit', 'учше', 'esc', 'close', '3'): 'exit',
                          ('load', 'дщфв', '1'): 'load',
                          ('new', 'туц', '2'): 'new'}

GUESS_COMMANDS = {('a', 'ad', 'addd', 'asd', 'asdd', 'sdd', 'adf', 'фів', 'івв',
                   'фівв', 'фввв', 'фва', 'вв', 'ыва', 'фвы', 'фыв', 'явв', 'фв'): 'add',

                  ('chane', 'chnge', 'cange', 'chenge', 'hange', 'chng', 'cchenge', 'chhenge',
                  'cheenge', 'chaange', 'сменить', 'chang', 'срутпу', 'срутп', 'менять', 'изменить',
                   'срфтп', 'рсфтпу', 'срутпу', 'cheng'): 'change',

                  ('fnd', 'ind', 'fid', 'fin', 'faind', 'fand', 'ffind', 'fiind', 'finnd', 'findd',
                   'seek', 'look', 'look for', 'атв', 'афтв', 'штв', 'афт', 'поиск', 'искать',
                   'найти', 'шштв'): 'find',

                  ('&', '?', 'hlp', 'what', 'why', 'where', 'how', 'elp', 'hep', 'hel', 'healp',
                   'halp', 'hhelp', 'heelp', 'hellp', 'helpp', 'рфдз', 'рдз', 'руз', 'руд',
                   'помощь'): 'help',

                  ('вуд', '-', 'del', 'вудуеу', 'вуфдуеу', 'dealete', 'elete', 'elet',
                   'delet', 'dlte', 'dlt', 'lete', 'dealete', 'вудуе', 'удалить',
                   'pop'): 'delete',

                  ('lf', 'birsday', 'bersday', 'bezday', 'bethday', 'birzday', 'bearsday',
                  'birthdey', 'beersday', 'brthday', 'иууксвфн', 'ишквфн', 'др',
                   'рождение', 'бездей', 'бирсдей', 'днюха', 'birthday people', 'birthday boy',
                   'birthday girl', 'birthda', 'birtda', 'birth', 'иуервфн', 'иуівфн',
                   'birt'): 'birthday',

                  ('cleen', 'clan', 'clin', 'cleane', 'cleene', 'klin', 'klean', 'lean', 'clen',
                   'kleen', 'суф', 'лдуут', 'лдуфт', 'сдуфту', 'клн', 'клин', 'разобрать',
                   'мусор'): 'clean',

                  ('ырща', 'ырщцу', 'showe', 'schow', 'schove', 'chov', 'shove', 'schov',
                   'schowe', 'how', 'sho', 'shouv', 'шов', 'ірщцу', 'показать', 'рщц',
                   'ірщм'): 'show'}


class Controller:

    def __init__(self):
        self.model = Model()
        self.view = ConsoleView()

    # @error_handler
    def add(self):
        # Ввод имени
        self.view.notify_of_message(100*'_')
        name = self.view.input_name()
        if name in EXIT_DECISION:
            self.view.esc_e = False
            self.view.notify_of_message("Not saved")
            return None

        birthday = None
        while True:
            # ввод дня рождения
            decision = self.view.ask_to_add_field('Birthday')

            if decision in YES_DECISION:

                birthday = self.view.input_birthday()
                if self.model.book.validate_birthday(birthday):
                    birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
                    break
                else:
                    self.view.notify_of_message(
                        'Wrong Birthday. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(name=name, birthday=birthday)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break

            else:
                self.view.notify_of_message('Wrong input!')

        address = None
        while True:
            # ввод адреса
            decision = self.view.ask_to_add_field('address')

            if decision in YES_DECISION:
                address = self.view.input_address()
                # валидация адреса
                if self.model.book.validate_address(address):
                    break
                else:
                    self.view.notify_of_message(
                        f'Your Address is {len(address)} symbols. Please no more than 30 symbols')
            elif decision in EXIT_DECISION:
                self.model.book.add_record(
                    name=name, birthday=birthday, address=address)
                self.view.esc_e = False
                self.view.say_buy()
                return None
            elif decision in NO_DECISION:
                break
            else:
                self.view.notify_of_message('Wrong input!')

        email = None
        while True:
            # ввод ємейла
            decision = self.view.ask_to_add_field('e-mail')
            if decision in YES_DECISION:
                email = self.view.input_email()
                # валидация ємейла
                if self.model.book.validate_email_format(email):
                    if self.model.book.validate_email_duration(email):
                        break
                    else:
                        self.view.notify_of_message(
                            f'Your E-mail is {len(email)} symbols. Please no more than 30 symbols')
                else:
                    self.view.notify_of_message(
                        'Format is wrong. Try again in format: your_nickname@something.domen_name')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(
                    name=name, birthday=birthday, address=address, email=email)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break

            else:
                self.view.notify_of_message('Wrong input!')

        tags = None
        while True:
            # ввод ТЄГА
            decision = self.view.ask_to_add_field('tags')
            if decision in YES_DECISION:
                tags = self.view.input_tags()
                # валидация тегов
                if self.model.book.validate_tags(tags):
                    break
                else:
                    self.view.notify_of_message(
                        f'Your Tags is {len(tags)} symbols. Please no more than 15 symbols')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(
                    name=name, birthday=birthday, address=address, email=email, tags=tags)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break
            else:
                self.view.notify_of_message('Wrong input!')

        phones = []
        while True:
            # ввод телефона
            decision = self.view.ask_to_add_field('phone-number')
            if decision in YES_DECISION:
                phone = self.view.input_phone()
                # валидация телефона
                if self.model.book.validate_phone(phone):
                    phones.append(phone)
                    print(f'Список телефонов - {phones}')
                else:
                    self.view.notify_of_message(
                        'Wrong input! Phone may start with + and has from 3 to 12 digits max. Example +380501234567')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(
                    name=name, birthday=birthday, address=address, tags=tags, phones=phones)
                self.view.esc_e = False
                self.view.say_buy()
                return None
            elif decision in NO_DECISION:
                break
            else:
                self.view.notify_of_message('Wrong input!')

        self.model.book.add_record(
            name=name, birthday=birthday, address=address, email=email, tags=tags, phones=phones)
        return None

    # @error_handler
    def change(self):
        # определяем id контакта что надо изменить
        self.view.notify_of_message(100*'_')
        find_v = self.view.input_name(
            message="Input name or keyword that you want to change")
        find_v = find_v.lower()
        records_list = self.model.book.find_value(find_v)

        if records_list:
            # если поиск дал результат
            self.view.notify_of_message(
                f"I've found {len(records_list)} notes with this word")
            self.show_find(records_list)
            # ввод id для редактирования
            edited_id = self.view.input_id()
        else:
            # если поиск не дал результата
            self.view.notify_of_message(
                f"The contact with name {find_v.upper()} is not found")
            return None
        # узнаем какое поле на какое значение надо изменить
        changed_field = self.view.input_field_to_edit()
        # вводим новое значение поля
        inputing_command = {1: self.view.input_name,
                            2: self.view.input_phone,
                            3: self.view.input_birthday,
                            4: self.view.input_address,
                            5: self.view.input_email,
                            6: self.view.input_tags}
        new_field_value = inputing_command[changed_field]()
        # вносим изменения
        executing_command = {1: self.model.book.edit_name,
                             2: self.model.book.edit_phone,
                             3: self.model.book.edit_birthday,
                             4: self.model.book.edit_address,
                             5: self.model.book.edit_email,
                             6: self.model.book.edit_tags
                             }
        result = executing_command[changed_field](edited_id, new_field_value)
        self.view.notify_of_message("This contact updates to DB:")
        print(result)

    @error_handler
    def clean_folder(self):
        user_input = self.view.enter_path_for_clean_lolder()
        path = pathlib.Path(user_input)
        CleanFolder().print_recursive(path, user_input)
        CleanFolder().delete_dir(user_input)
        self.view.notify_of_message(
            'Everything done! Please check your folder!')

    # @error_handler
    def birthday(self):

        self.view.notify_of_message(100*'_')
        decision = self.view.input_birthday_search_type()
        result = []

        if decision == 1:
            n = self.view.input_for_birthday_1()
            bday, result = self.model.book.find_persons_with_birthday_in_n_days(
                n)
            if result:
                self.view.notify_of_message(
                    f'On {bday} you need to congratulate {len(result)} people from your Addressbook')
                self.show_find(result)
            else:
                self.view.notify_of_message(
                    f'You need to congratulate noone on {bday}')

        elif decision == 2:
            n = self.view.input_for_birthday_2()
            result = self.model.book.find_persons_with_birthday_during_n_days(
                n)
            if len(result) > 0:
                print(
                    f'In future {n} days you need to congratulate {len(result)} people from your Addressbook')
                self.show_find(result)
            else:
                print(
                    f'In future {n} days nobody from your Addressbook will have birthday')

        elif decision == 3:
            name = self.view.input_for_birthday_3()
            result = self.model.book.find_persons_birthday(name)

            if result:
                self.view.print_persons_and_their_birthday(result)
            else:
                self.view.notify_of_message(
                    'No information about birthday. Please enter valid information using command "change" or add new person to Addressbook')

        elif decision == 4 or decision in EXIT_DECISION:
            self.view.esc_e = False
            self.view.say_buy()

        else:
            self.view.notify_of_message('This Name is not found!')

    # @error_handler
    def delete(self):
        self.view.notify_of_message(100*'_')
        keyword = self.view.input_name(
            message="Put Name, you want to find and delete from your addressbook")
        keyword = keyword.lower()
        # находим список объектов Record имя которых содержит keyword
        records_list = self.model.book.find_value(keyword)

        if records_list:
            # если поиск дал результат
            self.view.notify_of_message(
                f"I've found {len(records_list)} notes with this Name")
            self.show_find(records_list)
            # ввод id для удаления
            del_input = self.view.input_id()
            result = self.model.book.remove_record(del_input)
            self.view.notify_of_message("This contact deletes to DB:")
            print(result)
        else:
            self.view.notify_of_message(
                f"The contact with name {keyword.upper()} is not found")

    # @error_handler
    def find(self):
        self.view.notify_of_message(100*'_')
        find_v = self.view.input_name(
            message="Put word, half of word you want to find")
        result = self.model.book.find_value(find_v)
        self.view.notify_of_message("I've found following:")
        self.show_find(result)

    # @error_handler
    def show_find(self, records_list):
        # печатает результаты поиска
        number = len(records_list)
        iter = self.model.book.iterator(records_list, number)
        for i in iter:
            self.view.show_one_page_of_addressbook(i)

    # @error_handler
    def exit(self):
        self.view.esc_e = False
        self.view.say_buy()

    # @error_handler
    def show(self):
        number = self.view.enter_number_of_page()
        records_list = self.model.book.return_all_records()
        iter = self.model.book.iterator(records_list, number)

        for i in iter:
            self.view.show_one_page_of_addressbook(i)

        self.view.notify_of_message("The end of the contacts book")

    ##############################################################
    # Команды для Handler для работы с NotesBook

    # @error_handler
    def add_note(self):
        text, hashtag = self.view.add_note()
        self.model.notes_book.add_note(text, hashtag)
        self.view.notify_of_message("Your note is successfully saved")

    # @error_handler
    def delete_note(self):
        hashtag = self.view.delete_note()
        self.model.notes_book.delete_note(hashtag)
        self.view.notify_of_message(
            f"The note with hashtag '{hashtag}' is deleted")

    # @error_handler
    def edit_note(self):
        hashtag = self.view.input_hashtag_to_edit_notes()
        old_note_text = self.model.notes_book.find_note_for_editing(hashtag)
        new_note_text = self.view.edit_note(old_note_text)
        self.model.notes_book.edit_note(hashtag, new_note_text)
        self.view.notify_of_message(
            f'The note with tag {hashtag.upper()} is edited')

    # @error_handler
    def find_note(self):
        keyword = self.view.find_note()
        note_list = self.model.notes_book.find_note(keyword)

        if note_list:
            self.model.notes_book.print_notes(note_list)
            self.view.notify_of_message("The search is sucessfully finished")
        else:
            self.view.notify_of_message("Keyword is not found")

    # @error_handler
    def sort_notes(self):
        search_type = self.view.sort_notes()
        self.model.notes_book.print_notes(
            self.model.notes_book.sort_notes(search_type))

    # @error_handler
    def show_notes(self):
        self.view.notify_of_message('Your Notes Book:')
        self.model.notes_book.print_notes(self.model.notes_book.all_notes())

    # Конец конец команд для NotesBook
    # @error_handler
    def help_func(self):
        self.view.help()

    # @error_handler
    def handler(self, user_inpu):

        COMMANDS = {'add': self.add, 'ad': self.add, '+': self.add, 'фвв': self.add, 'change': self.change, 'срфтпу': self.change, 'close': self.exit, 'exit': self.exit, 'учше': self.exit,
                    'find': self.find, 'аштв': self.find, 'help': self.help_func, 'рудз': self.help_func, 'хелп': self.help_func, 'show': self.show, 'ырщц': self.show, 'ірщц': self.show,
                    'delete': self.delete, 'del': self.delete, 'вуд': self.delete, 'вудуеу': self.delete, 'birthday': self.birthday, 'ишкервфн': self.birthday, 'clean': self.clean_folder, 'сдуфт': self.clean_folder,
                    'add note': self.add_note, 'фвв тщеу': self.add_note, 'delete note': self.delete_note, 'вудуеу тщеу': self.delete_note, 'edit note': self.edit_note, 'увше тщеу': self.edit_note,
                    'find note': self.find_note, 'аштв тщеу': self.find_note, 'sort notes': self.sort_notes, 'ыщке тщеуы': self.sort_notes, 'show notes': self.show_notes, 'ырщц тщеуы': self.show_notes}

        if user_inpu in COMMANDS.keys():
            # если ввод команды понятный:
            return COMMANDS[user_inpu]()
        else:
            # если ввод команды не понятен - мы уточняем у пользователядщф
            for key, value in GUESS_COMMANDS.items():
                if user_inpu in key:
                    guess_command = value
                    if self.view.clarify_command(guess_command):
                        return COMMANDS[guess_command]()
            return self.view.notify_of_error()
