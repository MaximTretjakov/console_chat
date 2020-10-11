"""
2. Задание
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):

    with open('orders.json', 'r', encoding='utf-8') as from_file:
        data = json.load(from_file)

    with open('orders.json', 'w', encoding='utf-8') as to_file:
        orders_list = data['orders']
        order_info = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date
        }
        orders_list.append(order_info)
        json.dump(data, to_file, indent=4)


write_order_to_json('printer', '1', '2000', 'Ivanov I.I.', '07.10.2020')