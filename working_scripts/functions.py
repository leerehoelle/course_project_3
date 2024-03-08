import json
import os
from datetime import datetime
from os.path import join, dirname


def load_transactions(input_file_path):
    with open(input_file_path, 'r') as file:
        return json.load(file)

def filtration_executed(data):
    output_executed = [x for x in data if x and x['state'] == 'EXECUTED']
    return output_executed


def executed_sorted(output_executed):
    output_executed_sorted = sorted(output_executed, key=lambda x: datetime.fromisoformat(x["date"]), reverse=True)
    return output_executed_sorted[:5]

def mask_number(number: str) -> str:
    if number.startswith('Счет'):
        return f'Счет **{number[-4:]}'
    else:
        name, digits = number.rsplit(' ', 1)
        return f'{name} {digits[:4]} {digits[4:6]}** **** {digits[-4:]}'


def format_transaction(date, description, acc_to, amount, currency, acc_from=None) -> str:
    if acc_from:
        acc_from = mask_number(acc_from)
    acc_to = mask_number(acc_to)
    if acc_from:
        acc_string = f'{acc_from} -> {acc_to}'
    else:
        acc_string = acc_to
    return (f'{datetime.fromisoformat(date).strftime("%d.%m.%Y")} {description}\n'
            f'{acc_string}\n'
            f'{amount} {currency}')


def print_transactions(filtered_json_data: list[dict]):
    for transaction in filtered_json_data:
        print(format_transaction(
            transaction['date'],
            transaction['description'],
            transaction['to'],
            transaction['operationAmount']['amount'],
            transaction['operationAmount']['currency']['name'],
            transaction.get('from')
        ))
        print()


ROOT_DIR = dirname(dirname(__file__))
data_path = join(ROOT_DIR, 'operations.json')


print_transactions(executed_sorted(filtration_executed(load_transactions(data_path))))
