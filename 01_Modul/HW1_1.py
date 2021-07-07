# Напишите класс метакласс Meta,
# который всем классам для кого он будет метаклассом устанавливает порядковый номер.

NUMBER_OF_CLASSES = 0


class Meta(type):
    # мета класс, который всем классам для которого он будет метаклассом
    # устанавливает порядковый номер

    def __new__(meta_class, class_name, parents, attributes):
        global NUMBER_OF_CLASSES
        attributes['class_number'] = NUMBER_OF_CLASSES
        NUMBER_OF_CLASSES += 1
        print(f'Meta __new__ called with {attributes}')
        return type.__new__(meta_class, class_name, parents, attributes)


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)
