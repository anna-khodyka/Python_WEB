from threading import Thread
from time import sleep


class TestThread (Thread):
    # класс потока
    def __init__(self):
        super().__init__()  # если переопределяем init надо инициировать родительский класс

    def run(self):
        # для класса-потока (многопоточности) надо обязательно
        # определить функцию run которая будет выполняться в другом, отдельном потоке
        # sleep(1)
        self.print_hello()

    def print_hello(self):
        for i in range(3):
            print("Hello!")


thread = TestThread()
thread.start()  # чтобы запустить поток надо вызвать метод start
# который принадлежит родительскому классу Thread
for i in range(20):
    print(1)
thread.join()  # основной поток ждет когда закончится доп поток
print('After join')
