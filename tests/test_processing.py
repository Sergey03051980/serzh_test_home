# tests/test_processing.py
import pytest
from datetime import datetime
from src.pythonproject.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-01-01'},
        {'id': 2, 'state': 'CANCELED', 'date': '2023-01-02'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-01-03'}
    ]

def test_filter_by_state(sample_data):
    # Тест фильтрации по EXECUTED
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert all(op['state'] == 'EXECUTED' for op in result)

    # Тест фильтрации по CANCELED
    result = filter_by_state(sample_data, 'CANCELED')
    assert len(result) == 1
    assert result[0]['id'] == 2

def test_sort_by_date(sample_data):
    # Тест сортировки по убыванию (новые сначала)
    result = sort_by_date(sample_data)
    assert [op['id'] for op in result] == [3, 2, 1]

    # Тест сортировки по возрастанию
    result = sort_by_date(sample_data, reverse=False)
    assert [op['id'] for op in result] == [1, 2, 3]

def test_edge_cases():
    # Тест с пустым списком
    assert filter_by_state([]) == []
    assert sort_by_date([]) == []

    # Тест с некорректными данными
    with pytest.raises(TypeError):
        filter_by_state("not a list")
    with pytest.raises(TypeError):
        sort_by_date({"invalid": "data"})
