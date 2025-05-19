# src/pythonproject/generators.py
from typing import Iterator, Dict, List, Any


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по указанной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты (например, "USD")

    Yields:
        Словари транзакций с указанной валютой

    Examples:
        >>> list(filter_by_currency([{"operationAmount": {"currency": {"code": "USD"}}}], "USD"))
        [{'operationAmount': {'currency': {'code': 'USD'}}}]
    """
    for transaction in transactions:
        try:
            if transaction['operationAmount']['currency']['code'] == currency.upper():
                yield transaction
        except (KeyError, TypeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание каждой транзакции

    Examples:
        >>> list(transaction_descriptions([{"description": "Payment"}]))
        ['Payment']
    """
    for transaction in transactions:
        try:
            yield transaction['description']
        except KeyError:
            continue


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в указанном диапазоне.

    Args:
        start: Начальный номер (от 1)
        end: Конечный номер (до 9999999999999999)

    Yields:
        Номера карт в формате "XXXX XXXX XXXX XXXX"

    Examples:
        >>> list(card_number_generator(1, 2))
        ['0000 0000 0000 0001', '0000 0000 0000 0002']
    """
    for num in range(start, end + 1):
        yield f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " + \
            f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16]
