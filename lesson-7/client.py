import argparse
import logging
import sys
import json
import socket
import time
import logs.client_log_config
from decos import log
from errors import ServerError, ReqFieldMissingError

from helper.variables import (
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR,
    DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_PACKAGE_LENGTH, ENCODING, MESSAGE, MESSAGE_TEXT, SENDER
)

CLIENT_LOGGER = logging.getLogger('client_logger')


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                               f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


class ClientSocket:
    def __init__(self, af_inet, sock_stream, account_name='Guest'):
        self.inet = af_inet
        self.stream = sock_stream
        self.account_name = account_name

    @log
    def create_socket(self):
        CLIENT_LOGGER.debug(f'Создаем сокет клиента')
        return socket.socket(self.inet, self.stream)

    @log
    def create_presence(self):
        # Функция генерирует запрос о присутствии клиента
        # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name
            }
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.account_name}')
        return out

    @log
    def get_message(self, client):
        """
         Утилита приёма и декодирования сообщения
        принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
        """
        CLIENT_LOGGER.debug(f'ВЫзвана функция get_message клиента')
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
            CLIENT_LOGGER.error(error.args)

    @log
    def send_message(self, sock, message):
        # Утилита кодирования и отправки сообщения принимает словарь и отправляет его
        CLIENT_LOGGER.debug(f'Вызвана функция send_message клиента. Сообщение {message}.')
        try:
            js_message = json.dumps(message)
            encoded_message = js_message.encode(ENCODING)
            sock.send(encoded_message)
        except Exception as error:
            CLIENT_LOGGER.error(error.args)

    @log
    def process_ans(self, message):
        # Функция разбирает ответ сервера
        CLIENT_LOGGER.debug(f'Вызвана функция process_ans клиента. Сообщение {message}.')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            elif message[RESPONSE] == 400:
                raise ServerError(f'400 : {message[ERROR]}')
        raise ReqFieldMissingError(RESPONSE)

    @log
    def create_message(self, sock, account_name='Guest'):
        """Функция запрашивает текст сообщения и возвращает его.
        Так же завершает работу при вводе подобной комманды
        """
        message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
        if message == '!!!':
            sock.close()
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            print('Спасибо за использование нашего сервиса!')
            sys.exit(0)
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: account_name,
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        return message_dict

    @log
    def message_from_server(self, message):
        """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
        if ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and MESSAGE_TEXT in message:
            print(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        else:
            CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


def main():
    server_address, server_port, client_mode = arg_parser()
    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        cs = ClientSocket(socket.AF_INET, socket.SOCK_STREAM)
        sock = cs.create_socket()
        sock.connect((server_address, server_port))
        cs.send_message(sock, cs.create_presence())
        answer = cs.process_ans(cs.get_message(sock))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    cs.send_message(sock, cs.create_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    cs.message_from_server(cs.get_message(sock))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
