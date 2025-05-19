from typing import List, Dict, Any, Literal
from datetime import datetime


def filter_by_state(
        operations: List[Dict[str, Any]],
        state: Literal["EXECUTED", "CANCELED", "PENDING"] = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует операции по статусу.

    Args:
        operations: Список операций
        state: Статус для фильтрации (по умолчанию "EXECUTED")

    Returns:
        Отфильтрованный список операций

    Examples:
        >>> filter_by_state([{"state": "EXECUTED"}])
        [{'state': 'EXECUTED'}]
    """
    if not isinstance(operations, list):
        raise TypeError("Ожидается список операций")
    return [op for op in operations if op.get("state") == state]


def sort_by_date(
        operations: List[Dict[str, Any]],
        reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует операции по дате.

    Args:
        operations: Список операций
        reverse: Если True - новые сначала (по умолчанию)

    Returns:
        Отсортированный список операций

    Examples:
        >>> sort_by_date([{"date": "2023-01-01"}, {"date": "2023-01-02"}])
        [{'date': '2023-01-02'}, {'date': '2023-01-01'}]
    """
    if not isinstance(operations, list):
        raise TypeError("Ожидается список операций")

    def get_date(op):
        try:
            return datetime.fromisoformat(op["date"])
        except (KeyError, ValueError, TypeError):
            return datetime.min if reverse else datetime.max

    return sorted(operations, key=get_date, reverse=reverse)
