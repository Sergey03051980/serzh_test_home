import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import re

def profitable_cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> Dict[str, float]:
    """Анализ выгодных категорий для кешбэка."""
    result = {}
    for transaction in data:
        trans_date = datetime.strptime(transaction["Дата операции"], "%Y-%m-%d")
        if trans_date.year == year and trans_date.month == month:
            category = transaction["Категория"]
            cashback = transaction.get("Кешбэк", 0)
            result[category] = result.get(category, 0) + cashback
    return result

def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Расчет суммы для инвесткопилки."""
    total = 0.0
    year, month = map(int, month.split('-'))
    for trans in transactions:
        trans_date = datetime.strptime(trans["Дата операции"], "%Y-%m-%d")
        if trans_date.year == year and trans_date.month == month:
            amount = trans["Сумма операции"]
            rounded = ((amount + limit - 1) // limit) * limit
            total += rounded - amount
    return round(total, 2)

def simple_search(query: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Простой поиск по транзакциям."""
    return [t for t in transactions
            if query.lower() in t["Описание"].lower()
            or query.lower() in t["Категория"].lower()]

def find_phone_numbers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Поиск транзакций с телефонными номерами."""
    phone_regex = re.compile(r'\+7\s?\d{3}\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}')
    return [t for t in transactions if phone_regex.search(t["Описание"])]

def find_person_transfers(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Поиск переводов физлицам."""
    person_regex = re.compile(r'[А-Я][а-я]+\s[А-Я]\.')
    return [t for t in transactions
            if t["Категория"] == "Переводы"
            and person_regex.search(t["Описание"])]
