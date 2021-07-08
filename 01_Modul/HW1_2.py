# Напишите классы сериализации контейнеров с данными Python в json, bin файлы.
# Контейнеры: set, list, dict, tuple

# Сами классы должны соответствовать общему интерфейсу(абстрактному базовому классу)
# SerializationInterface.

from abc import ABC, abstractmethod
import json
import pickle

FILE_FORMAT = 'json'
BIN_FILE_NAME = 'Containers.bin'
JSON_FILE_NAME = 'Containers.json'


class SerializationInterface(ABC):
    # Класс интерфейс для классов сериализации
    def __init__(self, data) -> None:
        self.data = data

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass

# классы сериализации


class BinSerialization(SerializationInterface):
    # класс для сериализации всех контейнеров в bin
    def serialize(self):
        with open(BIN_FILE_NAME, 'wb') as f:
            pickle.dump(self.data, f)

    def deserialize(self):
        with open(BIN_FILE_NAME, 'rb') as f:
            self.data = pickle.load(f)


class SetToBinSerialization(BinSerialization):
    pass


class TupleToBinSerialization(BinSerialization):
    pass


class ListToBinSerialization(BinSerialization):
    pass


class DictToBinSerialization(BinSerialization):
    pass


class ListToJSONSerialization(SerializationInterface):
    # класс для сериализации списка в JSON
    def serialize(self):
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(self.data, f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            self.data = json.load(f)


class SetToJSONSerialization(SerializationInterface):
    # класс для сериализации множества в JSON: сначала переводит множество в список, потом сериализует
    def serialize(self):
        container = list(self.data)
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(container, f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            container = json.load(f)
            self.data = set(container)


class TupleToJSONSerialization(SerializationInterface):
    # класс для сериализации кортежа в JSON:
    # сначала переводит кортеж в список, потом сериализует
    def serialize(self):
        container = list(self.data)
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(container, f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            container = json.load(f)
            self.data = tuple(container)


class DictToJSONSerialization(SerializationInterface):
    # класс для сериализации словаря в JSON:
    # реализуем ситуацию когда ключ словаря - число
    def serialize(self):
        # создаем список позиций словаря, где ключом является не-строка
        non_str_position_dict = {}
        counter = 0
        for key in self.data:
            if isinstance(key, bool):
                non_str_position_dict[counter] = "bool"
            elif isinstance(key, float):
                non_str_position_dict[counter] = "float"
            elif isinstance(key, int):
                non_str_position_dict[counter] = "int"
            counter += 1
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump([self.data, non_str_position_dict], f)

    def deserialize(self):
        self.data = dict()
        non_str_position_dict = {}
        with open(JSON_FILE_NAME, 'r') as f:
            container, non_str_position_dict = json.load(f)
            # преобразовываем ключи, что д.б. не-строками:
            counter = 0
            for key, value in container.items():
                if str(counter) in non_str_position_dict.keys():
                    # если один из ключей не строка
                    if non_str_position_dict[str(counter)] == 'int':
                        self.data[int(key)] = value
                    elif non_str_position_dict[str(counter)] == 'float':
                        self.data[float(key)] = value
                    elif non_str_position_dict[str(counter)] == 'bool':
                        print(f'I have bool-key {key} {bool(key)}')
                        if key.lower() == 'true':
                            self.data[True] = value
                        elif key.lower() == 'false':
                            self.data[False] = value
                else:
                    self.data[key] = value
                counter += 1


def define_serialization_type(container):
    # является ли эта функция мета-функцией (возвращает объект класса)
    if FILE_FORMAT == 'bin':
        if isinstance(container, set):
            cls = SetToBinSerialization
        elif isinstance(container, tuple):
            cls = TupleToBinSerialization
        elif isinstance(container, list):
            cls = ListToBinSerialization
        elif isinstance(container, dict):
            cls = DictToBinSerialization
        else:
            raise TypeError("The container has a not defined type")
    elif FILE_FORMAT == 'json':
        if isinstance(container, set):
            cls = SetToJSONSerialization
        elif isinstance(container, tuple):
            cls = TupleToJSONSerialization
        elif isinstance(container, list):
            cls = ListToJSONSerialization
        elif isinstance(container, dict):
            cls = DictToJSONSerialization
        else:
            raise TypeError("The container has a not defined type")
    return cls(container)


if __name__ == '__main__':
    # список контейнеров для теста
    containers = [(1, 2, 3, 4, 5), {1, 2}, [1, 2, 3, 4], {
        "one": 1, 2.0: "2", False: 3, True: 225.56, 5: None}]
    # сами тесты
    for FILE_FORMAT in ('json', 'bin'):
        for container in containers:
            a_object = define_serialization_type(container)
            print(a_object.__class__.__name__)
            print(f'Контейнер до сериализации {container}')
            a_object.serialize()
            a_object.deserialize()
            print(f'Контейнер после десериализации {a_object.data}')
            assert container == a_object.data
