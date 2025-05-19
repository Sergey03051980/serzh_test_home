from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке.

    Args:
        account_info: Строка вида "Visa 1234567812345678" или "Счет 1234567890123456"

    Returns:
        Маскированная строка

    Raises:
        ValueError: Если входные данные невалидны
    """
    if not account_info or " " not in account_info:
        raise ValueError("Неверный формат входных данных")

    parts = account_info.rsplit(" ", 1)
    if "счет" in parts[0].lower():
        return f"{parts[0]} {get_mask_account(parts[1])}"
    return f"{parts[0]} {get_mask_card_number(parts[1])}"


def get_date(date_str: str) -> str:
    """
    Преобразует дату из ISO формата в DD.MM.YYYY.

    Args:
        date_str: Строка с датой в ISO формате

    Returns:
        Дата в формате DD.MM.YYYY

    Raises:
        ValueError: Если дата невалидна
    """
    try:
        return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")
    except (ValueError, TypeError) as e:
        raise ValueError("Неверный формат даты") from e


def print_operations(operations):
    """Печатает отсортированные операции с маскировкой (интеграция с processing.py)"""
    from .processing import \
        sort_by_date  # Локальный импорт во избежание циклических зависимостей

    for op in sort_by_date(operations):
        print(f"{get_date(op['date'])} {mask_account_card(op['description'])}")