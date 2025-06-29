import pandas as pd
import json
import requests
from datetime import datetime
import logging
from typing import Dict, List, Any
from flask import Flask, render_template
from pydantic import BaseModel, field_validator

# Инициализация Flask-приложения
app = Flask(__name__, template_folder='templates')

class DateRequest(BaseModel):
    date_str: str

    @field_validator('date_str')
    def validate_date_str(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM:SS")

@app.route('/')
def home_page():
    """Контроллер главной страницы"""
    return render_template('index.html', title='Home')

@app.route('/events')
def events_page():
    """Контроллер страницы событий"""
    return render_template('events.html', title='Events')


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
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        response.raise_for_status()
        rates = response.json()['rates']
        return [{"currency": curr, "rate": rates.get(curr, 0)} for curr in currencies]
    except Exception as e:
        logging.error(f"Currency API error: {e}")
        return [{"currency": curr, "rate": 0, "error": str(e)} for curr in currencies]


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

if __name__ == '__main__':
    app.run(debug=True)
