import pytest
from src.pythonproject.masks import get_mask_card_number, get_mask_account

@pytest.mark.parametrize("card_num,expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("1111222233334444", "1111 22** **** 4444"),
    ("", ""),  # Пустая строка
])
def test_get_mask_card_number(card_num, expected):
    if not card_num:
        with pytest.raises(ValueError):
            get_mask_card_number(card_num)
    else:
        assert get_mask_card_number(card_num) == expected

@pytest.mark.parametrize("account_num,expected", [
    ("1234567890", "**7890"),
    ("1234", "**1234"),
    ("12", ""),  # Слишком короткий
])
def test_get_mask_account(account_num, expected):
    if len(account_num) < 4:
        with pytest.raises(ValueError):
            get_mask_account(account_num)
    else:
        assert get_mask_account(account_num) == expected
