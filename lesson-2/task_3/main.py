"""
3. Задание 
"""

import yaml

data = {
    'key1': ['list', 'list', 'list', 'list'],
    'key2': 4,
    'key3': {
        'sub_key1': '1€',
        'sub_key2': '1€',
        'sub_key3': '1€',
        'sub_key4': '1€'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as to_file:
    yaml.dump(data, to_file, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as from_file:
    new_data = yaml.load(from_file, Loader=yaml.SafeLoader)

print(new_data)
