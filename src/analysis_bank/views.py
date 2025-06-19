import pandas as pd
import json
import requests
from datetime import datetime
import logging
from typing import Dict, List, Any


def get_greeting(time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют с API."""
    # Здесь должен быть реальный API-запрос
    return [{"currency": curr, "rate": 75.0} for curr in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций с API."""
    # Здесь должен быть реальный API-запрос
    return [{"stock": stock, "price": 100.0} for stock in stocks]


def main_page(date_str: str) -> Dict[str, Any]:
    """Главная страница - возвращает JSON с данными."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # Загрузка данных
        df = pd.read_excel("data/operations.xls")

        # Загрузка настроек
        with open("user_settings.json") as f:
            settings = json.load(f)

        # Формирование ответа
        return {
            "greeting": get_greeting(date),
            "cards": [],  # Здесь должна быть логика по картам
            "top_transactions": [],  # Топ транзакций
            "currency_rates": get_currency_rates(settings["user_currencies"]),
            "stock_prices": get_stock_prices(settings["user_stocks"])
        }
    except Exception as e:
        logging.error(f"Error in main_page: {e}")
        raise
