# Напишите класс метакласс Meta,
# который всем классам для кого он будет метаклассом устанавливает порядковый номер.

from abc import ABC, abstractmethod


class Meta(ABC):

    # мета класс, который всем классам для которого он будет метаклассом
    # устанавливает порядковый номер
    children_number = 0

    def __new__(meta_class, class_name, parents, attributes):
        attributes['class_number'] = Meta.children_number
        Meta.children_number += 1
        print(f'Meta __new__ called with {attributes}')
        return type.__new__(meta_class, class_name, parents, attributes)

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass


Meta.children_number = 0


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data

    def serialize(self):
        pass

    def deserialize(self):
        pass


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data

    def serialize(self):
        pass

    def deserialize(self):
        pass


assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)
