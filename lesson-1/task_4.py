"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""
from typing import List

words = ['разработка', 'администрирование', 'protocol', 'standard']


def encode_decode_custom(strings: List):
    for word in words:
        a = word.encode('utf-8')
        print(f'encode : {a}, Тип данных : {type(a)}')
        b = bytes.decode(a, 'utf-8')
        print(f'decode : {b}, Тип данных : {type(b)}')


if __name__ == '__main__':
    encode_decode_custom(words)
