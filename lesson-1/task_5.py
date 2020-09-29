"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
и преобразовать результаты из байтовового в строковый тип на кириллице.
"""
import subprocess
from typing import List

ping_list = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]


def ping_pong(commands: List):
    for ping in commands:
        ping_process = subprocess.Popen(ping, stdout=subprocess.PIPE)
        i = 0
        for line in ping_process.stdout:
            if i < 10:
                print(line)
                line = line.decode('cp866').encode('utf-8')
                print(line.decode('utf-8'))
                i += 1
            else:
                print('Zzzz... ZzZzzz... Zzzz...' * 30)
                break


if __name__ == '__main__':
    ping_pong(ping_list)
