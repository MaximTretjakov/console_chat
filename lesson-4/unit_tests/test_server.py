import unittest
import socket

from server import ServerSocket


class TestServer(unittest.TestCase):
    def test_ok_process_client_message(self):
        ss = ServerSocket(socket.AF_INET, socket.SOCK_STREAM)
        message = {
            'action': 'presence',
            'time': '1573760672.167031',
            'user': {
                'account_name': 'GUEST'
            }
        }
        self.assertNotEqual(ss.process_client_message(message), 200)

    def test_not_presence_process_client_message(self):
        ss = ServerSocket(socket.AF_INET, socket.SOCK_STREAM)
        message = {
            'action': 'quit',
            'user': {
                'account_name': 'GUEST'
            }
        }
        self.assertEqual(ss.process_client_message(message), 400)

    def test_not_guest_process_client_message(self):
        ss = ServerSocket(socket.AF_INET, socket.SOCK_STREAM)
        message = {
            'action': 'presence',
            'user': {
                'account_name': 'NOTGUEST'
            }
        }
        self.assertEqual(ss.process_client_message(message), 400)


if __name__ == '__main__':
    unittest.main()
