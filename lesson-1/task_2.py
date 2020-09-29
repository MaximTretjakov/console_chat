"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""
from typing import List

words = [b'class', b'function', b'method']


def info(strings: List):
    for string in strings:
        print(f'Байтовый формат | {string} | Тип {type(string)} | Длина {len(string)}')


if __name__ == '__main__':
    info(words)
