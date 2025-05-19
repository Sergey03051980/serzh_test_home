def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX

    Args:
        card_number: Номер карты (16 цифр)

    Raises:
        ValueError: Если номер не соответствует формату
    """
    if not isinstance(card_number, str) or not card_number.isdigit() or len(card_number) != 16:
        raise ValueError("Номер карты должен быть строкой из 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX

    Args:
        account_number: Номер счета (минимум 4 цифры)

    Raises:
        ValueError: Если номер не соответствует формату
    """
    if not isinstance(account_number, str) or not account_number.isdigit() or len(account_number) < 4:
        raise ValueError("Номер счета должен быть строкой минимум из 4 цифр")
    return f"**{account_number[-4:]}"
