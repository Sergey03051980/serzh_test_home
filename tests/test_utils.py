import pytest

from src.analysis_bank.utils import search_transactions_by_description, count_transactions_by_category


@pytest.fixture
def sample_transactions():
    return [
        {'description': 'Перевод организации', 'status': 'EXECUTED'},
        {'description': 'Открытие вклада', 'status': 'EXECUTED'},
        {'description': 'Перевод с карты на карту', 'status': 'CANCELED'},
    ]


def test_search_transactions_by_description(sample_transactions):
    result = search_transactions_by_description(sample_transactions, 'перевод')
    assert len(result) == 2
    assert all('Перевод' in t['description'] for t in result)


def test_count_transactions_by_category(sample_transactions):
    categories = ['Перевод организации', 'Открытие вклада']
    result = count_transactions_by_category(sample_transactions, categories)
    assert result == {'Перевод организации': 1, 'Открытие вклада': 1}
