import socket
from ipaddress import ip_address
from subprocess import Popen, PIPE


def check_host(ip_addresses, timeout=500, requests=1):
    results = {
        'Доступные хосты': '',
        'Недоступные хосты': ''
    }

    for address in ip_addresses:
        try:
            address = ip_address(address)
        except ValueError:
            address = socket.gethostbyname(address)

        proc = Popen(f'ping {address} -w {timeout} -n {requests}', shell=False, stdout=PIPE)
        proc.wait()
        if proc.returncode == 0:
            results['Доступные хосты'] += f'{str(address)}\n'
            res_string = f'{address} - Хост доступен'
        else:
            results['Недоступные хосты'] += f'{str(address)}\n'
            res_string = f'{address} - Хост недоступен'

        print(res_string)

    return results


if __name__ == '__main__':
    # call ipconfig
    ip_list = ['yandex.ru', '2.2.2.2', '192.168.1.70', '192.168.1.71']
    check_host(ip_list)
