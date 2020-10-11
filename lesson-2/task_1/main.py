"""
1. Задание
"""
import csv
import re


def get_data(files):
    result = {
        'Изготовитель системы': [],
        'Название ОС': [],
        'Код продукта': [],
        'Тип системы': []
    }
    main_data = [[*result.keys()]]

    for i in range(len(files)):
        main_data.append([i + 1])

    re_whitelist = re.compile(r'^(Изготовитель системы|Название ОС|Код продукта|Тип системы)')

    for file in files:
        with open(file, 'r', encoding='windows-1251') as f:
            for line in f:
                pairs = line.split(':')
                for pair in pairs:
                    if re_whitelist.search(pair):
                        result[pair].append(pairs[1].strip())

    for record in result.values():
        for num, v in enumerate(record):
            main_data[num + 1].append(record[num])

    return main_data


def write_to_csv(csv_file='data_report.csv'):
    data = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
    with open(csv_file, 'w') as final_file:
        writer = csv.writer(final_file)
        for row in data:
            writer.writerow(row)


write_to_csv()
