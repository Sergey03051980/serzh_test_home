import pytest
from src.services import profitable_cashback_categories
from datetime import datetime

@pytest.fixture
def sample_transactions():
    return [
        {
            "Дата операции": "2023-01-15",
            "Категория": "Супермаркеты",
            "Кешбэк": 50.0
        },
        {
            "Дата операции": "2023-01-20",
            "Категория": "Супермаркеты",
            "Кешбэк": 30.0
        },
        {
            "Дата операции": "2023-02-10",
            "Категория": "Рестораны",
            "Кешбэк": 20.0
        }
    ]

def test_profitable_cashback_categories(sample_transactions):
    result = profitable_cashback_categories(sample_transactions, 2023, 1)
    assert result == {"Супермаркеты": 80.0}
