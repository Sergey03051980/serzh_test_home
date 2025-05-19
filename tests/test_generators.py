# tests/test_generators.py
import pytest
from src.pythonproject.generators import *

def test_filter_by_currency(sample_transactions):
    usd = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd) == 1
    assert usd[0]["id"] == 1

def test_filter_edge_cases(edge_cases):
    assert len(list(filter_by_currency(edge_cases, "USD"))) == 0

def test_transaction_descriptions(sample_transactions):
    desc = list(transaction_descriptions(sample_transactions))
    assert desc == ["Payment 1", "Payment 2"]

@pytest.mark.parametrize("start,end,expected", [
    (1, 1, ["0000 0000 0000 0001"]),
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"])
])
def test_card_number_generator(start, end, expected):
    assert list(card_number_generator(start, end)) == expected
