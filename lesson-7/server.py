"""Программа-сервер"""
import logging
import select
import socket
import sys
import json
import time

import logs.server_log_config
from decos import log

from helper.variables import (
    ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE,
    TIME, USER, ERROR, DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING, MESSAGE, MESSAGE_TEXT, SENDER
)

SERVER_LOGGER = logging.getLogger('server_logger')


class ServerSocket:
    def __init__(self, af_inet, sock_stream):
        self.inet = af_inet
        self.stream = sock_stream

    @log
    def create_socket(self):
        SERVER_LOGGER.debug(f'Создаем сокет на сервере')
        return socket.socket(self.inet, self.stream)

    @log
    def get_message(self, client):
        """
         Утилита приёма и декодирования сообщения
        принимает байты выдаёт словарь, если принято что-то другое отдаёт ошибку значения
        """
        SERVER_LOGGER.debug(f'Вызвана функция get_message сервера')
        try:
            encoded_response = client.recv(MAX_PACKAGE_LENGTH)
            if isinstance(encoded_response, bytes):
                json_response = encoded_response.decode(ENCODING)
                response = json.loads(json_response)
                if isinstance(response, dict):
                    return response
                raise ValueError
            raise ValueError
        except Exception as error:
            SERVER_LOGGER.error(error.args)

    @log
    def send_message(self, sock, message):
        # Утилита кодирования и отправки сообщения принимает словарь и отправляет его
        SERVER_LOGGER.debug(f'Вызвана функция send_message сервера. Сообщение {message}')
        try:
            js_message = json.dumps(message)
            encoded_message = js_message.encode(ENCODING)
            sock.send(encoded_message)
        except Exception as error:
            SERVER_LOGGER.error(error.args)

    @log
    def process_client_message(self, message, messages_list, client):
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
        # Если это сообщение о присутствии, принимаем и отвечаем, если успех
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            self.send_message(client, {RESPONSE: 200})
            return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
        elif ACTION in message and message[ACTION] == MESSAGE and \
                TIME in message and MESSAGE_TEXT in message:
            messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
            return
        # Иначе отдаём Bad request
        else:
            self.send_message(client, {
                RESPONSE: 400,
                ERROR: 'Bad Request'
            })
            return


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет
    ss = ServerSocket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ss.create_socket()
    sock.bind((listen_address, listen_port))
    sock.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    sock.listen(MAX_CONNECTIONS)

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = sock.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    ss.process_client_message(ss.get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} 'f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    ss.send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
