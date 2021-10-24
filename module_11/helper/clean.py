'''модуль содержит класс CleanFolder'''
import re
import shutil
import os


class CleanFolder:
    '''содержит методы разборщика папок с хламов и сортировки файлов согласно их расширений'''

    @staticmethod
    def translate(string):
        """транслетирирует буквы кирилицы в латиницу"""
        cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
        translation = (
            "a",
            "b",
            "v",
            "g",
            "d",
            "e",
            "e",
            "j",
            "z",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "r",
            "s",
            "t",
            "u",
            "f",
            "h",
            "ts",
            "ch",
            "sh",
            "sch",
            "",
            "y",
            "",
            "e",
            "yu",
            "u",
            "ja",
            "je",
            "ji",
            "g",
        )

        trans = {}
        for c_letter, t_letter in zip(cyrillic_symbols, translation):
            trans[ord(c_letter)] = t_letter
            trans[ord(c_letter.upper())] = t_letter.upper()

        translated_string = string.translate(trans)

        return translated_string

    def normalize(self, string):
        """функция не только транслетерирует но и заменяет небуквы и нецифры на _"""

        normalized_string = self.translate(string)
        normalized_string = re.sub(
            r"[^0-9a-zA-Z ]", "_", normalized_string, flags=re.ASCII
        )

        return normalized_string

    def normalize_file_name(self, file_name):
        """функция нормализует название файла при этом не трогает расширение файла"""
        counter = 0
        normalized_file_name = ""
        for part in file_name.split("."):
            counter += 1
            if counter == len(file_name.split(".")):
                normalized_file_name += self.normalize(part)
            elif counter == len(file_name.split(".")) - 1:
                normalized_file_name = normalized_file_name + \
                    self.normalize(part) + "."
            else:
                normalized_file_name = normalized_file_name + \
                    self.normalize(part) + "_"
        return normalized_file_name

    def parse_recursion(self, folder_path, files_dict):
        '''парсинг папки рекурсивно'''
        extention_dict = {
            "images": {".jpeg", ".png", ".jpg", ".svg"},
            "video": {".avi", ".mp4", ".mov", ".mkv"},
            "documents": {".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"},
            "audio": {".mp3", ".ogg", ".wav", ".amr"},
            "archives": {".zip", ".gz", ".tar"},
        }

        # перебор всех объектов в папке и их анализ
        for folder_object in folder_path.iterdir():

            # если объект в папке - файл
            if folder_object.is_file():

                flag = False

                for file_type, file_ext_set in extention_dict.items():
                    if folder_object.suffix.lower() in file_ext_set:
                        if files_dict.get(file_type) is None:
                            files_dict[file_type] = []
                        files_dict[file_type].append(folder_object.absolute())
                        flag = True

                # если расширение файла не соотв не одному типу файлов со справочника
                if not flag:
                    if files_dict.get("others") is None:
                        files_dict["others"] = []
                    files_dict["others"].append(folder_object.absolute())

            # если объект в папке - папка, вызываем рекурсию
            if folder_object.is_dir():
                self.parse_recursion(folder_object, files_dict)

        return files_dict

    def move_files(self, root_folder, files_dict):
        '''перемещаем файлы в подпапки в зависимости от типа файла'''
        for file_type, files_list in files_dict.items():
            for file in files_list:
                # проверяем есть ли подпапка в названием типа файла, если нет - создаем ее
                if not (root_folder / file_type).exists():
                    os.makedirs(root_folder / file_type)

                # перемещаем файл в нужную подпапку
                if file_type != "archives":
                    # если файл не архив
                    normalized_file_name = self.normalize_file_name(file.name)
                    destination_path = root_folder / file_type / normalized_file_name
                    shutil.move(file, destination_path)
                else:
                    # перемещаем файл в нужную подпапку - если файл - архив
                    new_folder_for_archive = (
                        root_folder
                        / file_type
                        / self.normalize(file.name.removesuffix(file.suffix))
                    )
                    os.makedirs(new_folder_for_archive)
                    shutil.unpack_archive(file, new_folder_for_archive)
                    os.remove(file)

    def remove_empty_folders(self, folder_path):
        """удаляет все пустые подпапки в папке folder_path"""

        for folder_object in folder_path.iterdir():
            if folder_object.is_dir():
                if not os.listdir(folder_object):
                    os.removedirs(folder_object)
                else:
                    self.remove_empty_folders(folder_object)

    def parse_folder(self, folder_path):
        """функция разбирает папку согласно задания из ДЗ"""

        # проверка существует ли папка
        if folder_path.exists() is False:
            raise ValueError(
                f"The folder {folder_path.absolute()} is not existed"
            )
        if folder_path.exists() and (folder_path.is_dir() is False):
            raise ValueError(
                f"The path {folder_path.absolute()} is not a folder")
        # составляем каталог файлов, где ключ словаря - тип файла
        files_dict = {}
        files_dict = self.parse_recursion(folder_path, files_dict)
        # перемещаем файлы в подпапки в зависимости от типа файла
        self.move_files(folder_path, files_dict)
        # удаляет все пустые подпапки
        self.remove_empty_folders(folder_path)
