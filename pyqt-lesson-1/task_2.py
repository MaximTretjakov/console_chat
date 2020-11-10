from ipaddress import ip_address
from task_1 import check_host


def check_range_host():
    while True:
        start_ip = input('Введите первоначальный ip адрес :  ')
        try:
            last_oct = int(start_ip.split('.')[3])
            break
        except Exception as err:
            print(f'Error : {err.args}')

    while True:
        end_ip = input('Сколько адресов проверять?:  ')
        if not end_ip.isnumeric():
            print('Необходимо ввести число:  ')
        else:
            if (last_oct + int(end_ip)) > 254:
                print(f'Можем менять только последний октет, '
                      f'т.е. максимальное число для проверки: {254 - last_oct}')
            else:
                break

    host_list = []
    [host_list.append(str(ip_address(start_ip) + x)) for x in range(int(end_ip))]
    return check_host(host_list)


if __name__ == '__main__':
    check_range_host()
