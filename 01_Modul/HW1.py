# Напишите классы сериализации контейнеров с данными Python в json, bin файлы.
# Контейнеры: set, list, dict, tuple

# Сами классы должны соответствовать общему интерфейсу(абстрактному базовому классу)
# SerializationInterface.

# Напишите класс метакласс Meta,
# который всем классам для кого он будет метаклассом устанавливает порядковый номер.
from abc import ABC, abstractmethod

# глобальная переменная, хранит количество созданных классов, у которых метакласс Meta
NUMBER_OF_CLASSES = 0


class Meta(type):
    # мета класс, который всем классам для которого он будет метаклассом
    # устанавливает порядковый номер

    def __new__(meta_class, class_name, parents, attributes):
        global NUMBER_OF_CLASSES
        NUMBER_OF_CLASSES += 1
        attributes['class_number'] = NUMBER_OF_CLASSES
        print(f'Meta __new__ called with {attributes}')
        return type.__new__(meta_class, class_name, parents, attributes)


class SerializationInterface(ABC):
    # Класс интерфейс для классов сериализации
    def __init__(self, data) -> None:
        self.data = data

    @ abstractmethod
    def serialize(self):
        pass

    @ abstractmethod
    def deserialize(self):
        pass

# классы сериализации


class SetToBinSerialization(metaclass=Meta):

    def serialize(self):
        pass

    def deserialize(self):
        pass


class TupleToBinSerialization(metaclass=Meta):

    def serialize(self):
        pass

    def deserialize(self):
        pass


if __name__ == '__main__':
    a = SetToBinSerialization()
    b = TupleToBinSerialization()
    # тест-кейсы с помощью assert
