'''
Напишите реализацию функции factorize которая принимает список чисел 
и возвращает список чисел, на которые числа из входного списка делятся без остатка.

Реализуйте синхронную версию и измерьте время выполнения.

Потом улучшите производительность вашей функции 
реализовав использование нескольких ядер процессора для параллельных вычислений 
и замерьте время выполнения опять.
'''

import time
from multiprocessing import Pool


def factorize_number(number):
    # функция находит все делители числа number, возвращает список делителей
    n_result = []
    for i in range(1, number+1):
        if (number % i) == 0:
            n_result.append(i)
    return n_result


def factorize(*number):
    # последовательный код
    # функция находит все делители каждого числа из списка *number, возвращает список списков делителей
    results = []
    for n in number:
        results.append(factorize_number(n))
    return results


def multi_factorize(*number):
    # код с использованием мульти-процессов
    # функция находит все делители каждого числа из списка *number, возвращает список списков делителей
    with Pool(processes=2) as pool:
        results = pool.map(factorize_number, number)
    return results


if __name__ == "__main__":

    # test case for consistent code
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # test case for code with multiproccessing
    a, b, c, d = multi_factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print('Test cases are finished successfully')

    # using factorize functions

    # consistent code
    started = time.time()
    factorize(128, 255, 99999, 10651060, 45403940,
              34534334, 23434432, 73423424)
    elapsed = time.time() - started
    print(f'The time of consistent code - {elapsed}')

    # multiproccessing
    started = time.time()
    multi_factorize(128, 255, 99999, 10651060, 45403940,
                    34534334, 23434432, 73423424)
    elapsed = time.time() - started
    print(f'The time of code with multiproccessing - {elapsed}')
