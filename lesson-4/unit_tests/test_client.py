"""Тесты клиента"""
import unittest
import socket

from client import ClientSocket


class TestClass(unittest.TestCase):
    def test_no_account(self):
        cs = ClientSocket(socket.AF_INET, socket.SOCK_STREAM, account_name='Bob')
        self.assertNotEqual(cs.account_name, 'Bob', 'Введенное имя не распознается')


if __name__ == '__main__':
    unittest.main()
