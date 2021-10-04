import redis


class LruCache:
    def __init__(self, func, max_size):
        self.func = func
        self.max_size = max_size
        self._cache = redis.Redis()
        self._cache.flushall()
        self.queue = ""

    def __call__(self, *args, **kwargs):

        # извлекаем сигнатуру функции и переменных
        func_signature = self.func.__name__  # добавляем сигнатуру функции
        for a in args:
            # добавляем значение неименованных параметров
            func_signature += ":"+str(a)
        for value in kwargs.values():
            func_signature += ":"+value  # добавляем значение именованных параметров
        print(func_signature)

        # реализуем алгоритм LRU-cache
        if self._cache.get(func_signature):
            print('Значение есть в кєше')
            # возвращаем значение по ключу letter
            result = self._cache.get(func_signature)
            # удаляем из очереди letter
            self._cache.lrem(self.queue, -1, func_signature)
            # добавляем в начало очереди letter
            self._cache.lpush(self.queue, func_signature)
        else:
            print('Значения нет в кєше')
            # записываем в словарь значение по ключу letter
            result = self.func(*args, **kwargs)
            self._cache.set(func_signature, result)  # записываем в кэш
            # добавляем в начало очереди letter
            self._cache.lpush(self.queue, func_signature)
            # проверка: если длина очереди больше max-size то обрезаем список
            if self._cache.llen(self.queue) > self.max_size:
                last_element = self._cache.rpop(self.queue)
                self._cache.delete(last_element)

        return result


def lru_cache(max_size=5):
    def wrapper(func):
        cache = LruCache(func, max_size)
        return cache
    return wrapper


@ lru_cache()
def foo(value: str, value_1: int):
    return f'result_of_{value}_{value_1}'


if __name__ == '__main__':
    print(foo('Redis', value_1="testing"))
    print(foo(value='Redis', value_1="testing"))
    print(foo('Redis', "testing"))
