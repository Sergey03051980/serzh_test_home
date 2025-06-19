import logging
import re
from datetime import datetime
from typing import List, Dict, Any, TypedDict, Union

logger = logging.getLogger(__name__)

PHONE_PATTERN = re.compile(r"\+7\s?\d{3}\s?\d{3}[- ]?\d{2}[- ]?\d{2}")
PERSON_PATTERN = re.compile(r"^[А-Я][а-я]+\s[А-Я]\.$")
DATE_FORMAT = "%Y-%m-%d"


class Transaction(TypedDict, total=False):
    """Типизированный словарь для транзакций."""
    Дата_операции: str
    Категория: str
    Описание: str
    Сумма_операции: str
    Кешбэк: float
    Отправитель: str
    Получатель: str


def _validate_transaction(transaction: Union[Transaction, Dict[str, Any]], required_fields: List[str]) -> bool:
    """Проверяет наличие обязательных полей в транзакции."""
    missing_fields = [field for field in required_fields if field not in transaction]
    if missing_fields:
        logger.warning(f"Transaction missing required fields: {missing_fields}")
        return False
    return True


def find_person_transfers(
        transactions: List[Transaction],
        person_name: str,
        is_sender: bool = False
) -> List[Transaction]:
    """Находит переводы по имени отправителя/получателя"""
    field = 'Отправитель' if is_sender else 'Получатель'
    return [
        t for t in transactions
        if field in t and str(t[field]).lower() == person_name.lower()
    ]


def find_phone_transactions(
        transactions: List[Transaction],
        phone_pattern: str = r"\+7\s?\d{3}\s?\d{3}[- ]?\d{2}[- ]?\d{2}"
) -> List[Transaction]:
    """Находит транзакции, содержащие номер телефона в описании."""
    pattern = re.compile(phone_pattern)
    return [
        t for t in transactions
        if 'Описание' in t and pattern.search(t['Описание'])
    ]


def profitable_cashback_categories(
        data: List[Union[Transaction, Dict[str, Any]]],
        year: int,
        month: int
) -> Dict[str, float]:
    """Рассчитывает наиболее выгодные категории кешбэка."""
    result: Dict[str, float] = {}
    required_fields = ["Дата_операции", "Категория", "Кешбэк"]  # Добавили Кешбэк в обязательные поля

    for transaction in data:
        if not _validate_transaction(transaction, required_fields):
            continue

        try:
            trans_date = datetime.strptime(transaction["Дата_операции"], DATE_FORMAT)
            if trans_date.year == year and trans_date.month == month:
                category = transaction["Категория"]
                cashback = float(transaction["Кешбэк"])  # Убрали get(), так как поле проверено
                result[category] = result.get(category, 0.0) + cashback
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid transaction data: {e}")
            continue

    return {k: round(v, 2) for k, v in sorted(result.items(), key=lambda x: x[1], reverse=True)}


def investment_bank(
        month: str,
        transactions: List[Union[Transaction, Dict[str, Any]]],
        limit: int
) -> float:
    """Рассчитывает сбережения от округления транзакций."""
    total = 0.0
    required_fields = ["Дата_операции", "Сумма_операции"]

    try:
        year, month_val = map(int, month.split("-"))
        if not (1 <= month_val <= 12):
            raise ValueError("Month must be between 1 and 12")

        if limit <= 0:
            raise ValueError("Limit must be positive")

        for transaction in transactions:
            if not _validate_transaction(transaction, required_fields):
                continue

            try:
                trans_date = datetime.strptime(transaction["Дата_операции"], DATE_FORMAT)
                if trans_date.year == year and trans_date.month == month_val:
                    amount = float(transaction["Сумма_операции"])
                    if amount > 0:  # Добавили проверку на положительную сумму
                        rounded = ((int(amount) // limit) + 1) * limit
                        total += rounded - amount
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid transaction amount: {e}")
                continue

        return round(total, 2) if total > 0 else 0.0  # Гарантируем возврат 0.0 если нет операций

    except ValueError as e:
        logger.error(f"Invalid input parameters: {e}")
        return 0.0  # Возвращаем 0 вместо вызова исключения
    except Exception as e:
        logger.error(f"Unexpected error in savings calculation: {e}")
        return 0.0
