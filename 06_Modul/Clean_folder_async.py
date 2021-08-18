'''

Напишите программу обработки папки "Хлам", 
которая сортирует файлы в указанной папке по расширениям с использованием asyncio. 
Чтобы перемещать и переименовывать файлы воспользуйтесь асинхронной версией pathlib: aiopath.
'''

import asyncio
import pathlib
import shutil
import os
import re
import time

import aiopath

# константы для транслитерации
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

# словарь расширений
EXTENTION_DICT = {'images': {'.jpeg', '.png', '.jpg', '.svg', '.eps', '.ai'},
                  'video': {'.avi', '.mp4', '.mov', '.mkv'},
                  'documents': {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.xml', '.xls'},
                  'audio': {'.mp3', '.ogg', '.wav', '.amr'},
                  'archives': {'.zip', '.gz', '.tar'}}


def translate(string):
    # транслетирирует буквы кирилицы в латиницу
    return string.translate(TRANS)


def normalize(string):
    # функция не только транслетерирует но и заменяет небуквы и нецифры на _
    normalized_string = translate(string)
    normalized_string = re.sub(
        r'[^0-9a-zA-Z ]', '_', normalized_string, flags=re.ASCII)

    return normalized_string


def normalize_file_name(file_name):
    # функция нормализует название файла, не изменяя расширение файла
    counter = 0
    normalized_file_name = ''
    for part in file_name.split('.'):
        counter += 1
        if counter == len(file_name.split('.')):
            normalized_file_name += normalize(part)
        elif counter == len(file_name.split('.'))-1:
            normalized_file_name += normalize(part) + '.'
        else:
            normalized_file_name += normalize(part) + '_'
    return normalized_file_name


async def parse_recursion(folder_path, files_dict):
    # функция обходит содержимое папки, если есть подпапка - рекурсивно вызывает себя

    # перебор всех объектов в папке и их анализ
    async for object in folder_path.iterdir():

        # если объект в папке - файл
        # заносим путь файла в files_dict
        is_file = await object.is_file()
        if is_file:
            # определяем тип файла
            file_type = None
            for f_type, file_ext_set in EXTENTION_DICT.items():
                if object.suffix.lower() in file_ext_set:
                    file_type = f_type
            if not file_type:
                file_type = 'others'

            # если такой тип файлов попался первый раз
            # создаем в словаре новую запись
            if files_dict.get(file_type) == None:
                files_dict[file_type] = list()

            # делаем запись в словарь
            files_dict[file_type].append(object.absolute())

        # если объект в папке - папка, вызываем рекурсию
        is_folder = await object.is_dir()
        if is_folder:
            await parse_recursion(object, files_dict)
    return files_dict


async def move_file(root_folder, file, file_type):

    # перемещаем файл в нужную подпапку
    if file_type != 'archives':
        # если файл не архив
        normalized_file_name = normalize_file_name(file.name)
        destination_path = root_folder / file_type / normalized_file_name
        await file.replace(destination_path)
    else:
        # перемещаем файл в нужную подпапку - если файл - архив
        new_folder_for_archive = root_folder / file_type / \
            normalize(file.name.removesuffix(file.suffix))
        await aiopath.AsyncPath.mkdir(new_folder_for_archive)
        shutil.unpack_archive(file, new_folder_for_archive)
        await aiopath.AsyncPath.unlink(file)


async def move_files(folder_path, files_dict):
    # перемещаем файлы в подпапки в зависимости от типа файла
    for file_type, files_list in files_dict.items():
        for file in files_list:
            await move_file(folder_path, file, file_type)


async def remove_empty_folders(folder_path):
    # удаляет все пустые подпапки в папке folder_path
    async for object in folder_path.iterdir():
        is_folder = await object.is_dir()
        if is_folder:
            # проверка пустая ли папка - не знаю как это сделать с iopath
            if not os.listdir(object):
                os.removedirs(object)
            else:
                await remove_empty_folders(object)


async def parse_folder(folder_path):
    # функция переносит файлы в подпапки согласно типов файлов

    files_dict = dict()

    # создаем словарь с всеми файлами
    files_dict = await parse_recursion(folder_path, files_dict)
    # создаем подпапки с названиями типов файлов
    for file_type in files_dict:
        await aiopath.AsyncPath.mkdir(folder_path / file_type)
    # перемещаем файлы в подпапки в зависимости от типа файла
    await move_files(folder_path, files_dict)
    # удаляет все пустые подпапки
    await remove_empty_folders(folder_path)


if __name__ == "__main__":

    for i in range(10):
        # удаляем папку из предыдущего опыта
        if (pathlib.Path('D:\Hlam')).exists():
            shutil.rmtree(pathlib.Path('D:\Hlam'))
        # создаем папку для опыта
        folder_path = shutil.copytree('D:\Hlam_template', 'D:\Hlam')
        folder_path = aiopath.AsyncPath(folder_path)
        started = time.time()
        asyncio.run(parse_folder(folder_path))
        elapsed = time.time() - started
        print(elapsed)
