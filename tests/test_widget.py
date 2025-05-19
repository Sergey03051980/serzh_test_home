import pytest
from datetime import datetime
from src.pythonproject.widget import mask_account_card, get_date

@pytest.fixture
def sample_account_strings():
    return [
        "Visa Platinum 1234567890123456",  # Валидная карта
        "Счет 1234567890123456",           # Валидный счет
        "Maestro 1234567812345678",        # Другой тип карты
        "МИР 1234567890123456",            # Карта МИР
        "Invalid String Without Number",    # Невалидный формат
        "Счет 123",                        # Слишком короткий счет
        "",                                # Пустая строка
        None                               # None вместо строки
    ]

@pytest.fixture
def sample_dates():
    return [
        "2023-01-01T12:00:00",            # Полная дата
        "2023-12-31",                     # Только дата
        "invalid-date",                   # Невалидная дата
        "",                               # Пустая строка
        None                              # None
    ]

# Параметризованные тесты для mask_account_card
@pytest.mark.parametrize("input_str, expected", [
    ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ("Счет 1234567890123456", "Счет **3456"),
    ("Maestro 1234567812345678", "Maestro 1234 56** **** 5678"),
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
])
def test_mask_account_card_valid(input_str, expected):
    assert mask_account_card(input_str) == expected

@pytest.mark.parametrize("invalid_input", [
    "Invalid String Without Number",
    "Счет 123",
    "",
    None
])
def test_mask_account_card_invalid(invalid_input):
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)

# Параметризованные тесты для get_date
@pytest.mark.parametrize("date_str, expected", [
    ("2023-01-01T12:00:00", "01.01.2023"),
    ("2023-12-31", "31.12.2023"),
])
def test_get_date_valid(date_str, expected):
    assert get_date(date_str) == expected

@pytest.mark.parametrize("invalid_date", [
    "invalid-date",
    "",
    None
])
def test_get_date_invalid(invalid_date):
    with pytest.raises(ValueError):
        get_date(invalid_date)

# Тест для проверки сообщения об ошибке
def test_mask_account_card_error_message():
    with pytest.raises(ValueError, match="Неверный формат входных данных"):
        mask_account_card("Invalid")

