"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и
содержимое переменных.
"""
from typing import List

words_string = ['разработка', 'сокет', 'декоратор']
words_unicode = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
    '\u0441\u043e\u043a\u0435\u0442',
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
]


def info_words_string(words_s: List):
    for word in words_s:
        print(f'Строковый формат | {word} | Тип {type(word)}')


def info_words_unicode(words_u: List):
    for word in words_u:
        print(f'В кодовых точках | {word} | Тип {type(word)}')


if __name__ == '__main__':
    info_words_string(words_string)
    info_words_unicode(words_unicode)
    print(list(map(lambda x, y: x == y, words_unicode, words_string)))
