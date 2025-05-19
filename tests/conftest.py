import pytest
from datetime import datetime, timedelta
from typing import Dict, List, Any

@pytest.fixture
def sample_card_numbers() -> List[str]:
    """Фикстура с валидными и невалидными номерами карт"""
    return [
        "1234567890123456",  # valid
        "1111222233334444",  # valid
        "123",               # invalid (short)
        "abcdefghijklmnop",  # invalid (letters)
    ]

@pytest.fixture
def sample_account_numbers() -> List[str]:
    """Фикстура с валидными и невалидными номерами счетов"""
    return [
        "1234567890123456",  # valid
        "1234",              # valid (min length)
        "12",                # invalid (short)
        "abcdef",            # invalid (letters)
    ]

@pytest.fixture
def sample_account_strings() -> List[str]:
    """Фикстура с валидными и невалидными строками карт/счетов"""
    return [
        "Visa Platinum 1234567890123456",
        "Счет 1234567890123456",
        "Maestro 1234567890123456",
        "Invalid String Without Number",
        "Счет 123",  # invalid
    ]

@pytest.fixture
def sample_dates() -> List[str]:
    """Фикстура с валидными и невалидными датами"""
    return [
        "2023-01-01",
        "2023-12-31T23:59:59.999999",
        "invalid-date",
        "",
    ]

@pytest.fixture
def sample_operations() -> List[Dict]:
    """Фикстура с операциями для тестирования processing.py"""
    base_date = datetime.now()
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": (base_date - timedelta(days=1)).isoformat(),
            "description": "Visa 1234567890123456",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": (base_date - timedelta(days=2)).isoformat(),
            "description": "Счет 1234567890123456",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": (base_date - timedelta(days=3)).isoformat(),
            "description": "MasterCard 1234567890123456",
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "invalid-date",  # специально невалидная
            "description": "Invalid Operation",
        },
    ]

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            },
            "description": "Payment 1"
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200.00",
                "currency": {"code": "EUR"}
            },
            "description": "Payment 2"
        }
    ]

@pytest.fixture
def edge_cases() -> List[Dict[str, Any]]:
    return [
        {},
        {"operationAmount": {}},
        {"operationAmount": {"currency": {}}},
        None
    ]
