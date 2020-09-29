"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""
from typing import List

words = [b'attribute', b'класс', b'функция', b'type']


def convert(strings: List):
    for string in strings:
        print(f'Пробую вывести в байтах : {string}')


if __name__ == '__main__':
    convert(words)
