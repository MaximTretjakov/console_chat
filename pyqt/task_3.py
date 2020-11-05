from tabulate import tabulate
from task_2 import check_range_host


def check_range_host_tab():
    res_dict = check_range_host()
    print()
    print(tabulate([res_dict], headers='keys', tablefmt='pipe', stralign='center'))


if __name__ == '__main__':
    check_range_host_tab()
