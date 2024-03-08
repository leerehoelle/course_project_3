import json
import pytest
from working_scripts.functions import (
    load_transactions,
    filtration_executed,
    executed_sorted,
    mask_number,
    format_transaction,
    print_transactions)
from sample.sample import sample_json
from os.path import join, dirname

ROOT_DIR = dirname(dirname(__file__))
data_path = join(ROOT_DIR, 'operations.json')

@pytest.fixture
def sample_transactions(tmp_path):
    # Create a temporary JSON file for testing
    data = sample_json(data_path)
    file_path = tmp_path / 'test_input.json'
    with open(file_path, 'w') as file:
        json.dump(data, file)
    return str(file_path)

def test_load_transactions(sample_transactions):
    transactions = load_transactions(sample_transactions)
    assert isinstance(transactions, list)
    assert len(transactions) == 10


def test_filtration_executed():
    data = [
        {'state': 'EXECUTED'},
        {'state': 'CANCELED'},
        {'state': 'EXECUTED'},
    ]
    result = filtration_executed(data)
    assert len(result) == 2
    assert all(x['state'] == 'EXECUTED' for x in result)


def test_executed_sorted():
    data = [
        {'date': '2023-01-02T12:00:00'},
        {'date': '2023-01-01T12:00:00'},
        {'date': '2023-01-03T12:00:00'},
    ]
    result = executed_sorted(data)
    assert result == [
        {'date': '2023-01-03T12:00:00'},
        {'date': '2023-01-02T12:00:00'},
        {'date': '2023-01-01T12:00:00'},
    ]


def test_mask_number():
    assert mask_number('Счет1234') == 'Счет **1234'
    assert mask_number('Visa Classic 1234567812345678') == 'Visa Classic 1234 56** **** 5678'


def test_format_transaction():
    # Test case 1: Transaction from one account to another with currency specified
    date = '2023-01-01T12:00:00'
    description = 'Перевод с карты на карту'
    acc_to = 'Visa Classic 1234567890123456'
    amount = 100
    currency = 'USD'
    acc_from = 'Maestro 9876543210987654'
    expected_result = (
        '01.01.2023 Перевод с карты на карту\n'
        'Maestro 9876 54** **** 7654 -> Visa Classic 1234 56** **** 3456\n'
        '100 USD'
    )
    assert format_transaction(date, description, acc_to, amount, currency, acc_from) == expected_result


def test_print_transactions(capsys):
    test_data = [
        {
            'date': '2023-01-01T12:00:00',
            'description': 'Перевод с карты на карту',
            'to': 'Visa Classic 1234567890123456',
            'operationAmount': {'amount': 50, 'currency': {'name': 'USD'}},
            'from': 'Maestro 9876543210987654'
        }    ]
    print_transactions(test_data)
    captured = capsys.readouterr()
    assert captured.out == (
        '01.01.2023 Перевод с карты на карту\n'
        'Maestro 9876 54** **** 7654 -> Visa Classic 1234 56** **** 3456\n'
        '50 USD\n'
        '\n')
