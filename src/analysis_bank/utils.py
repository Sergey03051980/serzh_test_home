import logging
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_column_names(df):
    """Приводит названия столбцов к единому формату (заменяет пробелы на подчёркивания)"""
    df.columns = df.columns.str.replace(" ", "_")
    return df


import pandas as pd
import os


def load_transactions(filepath):
    """Загружает транзакции из файла"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл {filepath} не найден")

    try:
        if filepath.endswith('.json'):
            return pd.read_json(filepath)
        elif filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith(('.xlsx', '.xls')):
            return pd.read_excel(filepath)
        else:
            raise ValueError("Неподдерживаемый формат файла")
    except Exception as e:
        raise Exception(f"Ошибка при чтении файла: {str(e)}")


def filter_transactions_by_date(
        df: pd.DataFrame, date_str: str, date_range: str = "M"
) -> pd.DataFrame:
    """Filter transactions by date range.

    Args:
        df: DataFrame with transactions
        date_str: Date in format 'YYYY-MM-DD HH:MM:SS'
        date_range: Range to filter ('W', 'M', 'Y', 'ALL')

    Returns:
        Filtered DataFrame
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        df["Дата_операции"] = pd.to_datetime(df["Дата_операции"])

        if date_range == "W":
            start_date = date - pd.Timedelta(days=date.weekday())
        elif date_range == "M":
            start_date = date.replace(day=1)
        elif date_range == "Y":
            start_date = date.replace(month=1, day=1)
        elif date_range == "ALL":
            return df[df["Дата_операции"] <= date]

        return df[(df["Дата_операции"] >= start_date) & (df["Дата_операции"] <= date)]
    except Exception as e:
        logger.error(f"Error filtering transactions: {e}")
        raise


def get_greeting(time: datetime) -> str:
    """Return greeting based on time of day.

    Args:
        time: Datetime object

    Returns:
        Greeting string
    """
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def fetch_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Fetch currency rates from API.

    Args:
        currencies: List of currency codes to fetch

    Returns:
        List of dictionaries with currency rates
    """
    try:
        # Example API - replace with actual implementation
        results = []
        for currency in currencies:
            # Mock implementation - replace with real API call
            rate = 75.0 if currency == "USD" else 85.0
            results.append({"currency": currency, "rate": rate})
        return results
    except Exception as e:
        logger.error(f"Error fetching currency rates: {e}")
        return []


def fetch_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Fetch stock prices from API.

    Args:
        stocks: List of stock symbols to fetch

    Returns:
        List of dictionaries with stock prices
    """
    try:
        # Example API - replace with actual implementation
        results = []
        for stock in stocks:
            # Mock implementation - replace with real API call
            price = 150.0 if stock == "AAPL" else 3000.0
            results.append({"stock": stock, "price": price})
        return results
    except Exception as e:
        logger.error(f"Error fetching stock prices: {e}")
        return []


def home_page(date_str: str) -> Dict[str, Any]:
    """Generate data for home page."""
    try:
        # Load transactions
        df = load_transactions()
        logger.debug(f"Columns in DataFrame: {df.columns.tolist()}")

        # Filter transactions
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        df_filtered = filter_transactions_by_date(df, date_str)

        # Generate greeting
        greeting = get_greeting(date_obj)

        # Prepare response structure
        response = {
            "greeting": greeting,
            "cards": [],
            "top_transactions": [],
            "currency_rates": fetch_currency_rates(["USD", "EUR"]),
            "stock_prices": fetch_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        }

        # Calculate card statistics if data exists
        if not df_filtered.empty and "Номер_карты" in df_filtered.columns:
            for card in df_filtered["Номер_карты"].unique():
                card_df = df_filtered[df_filtered["Номер_карты"] == card]
                total_spent = card_df["Сумма_операции"].sum()
                response["cards"].append({
                    "last_digits": str(card)[-4:],
                    "total_spent": round(total_spent, 2),
                    "cashback": round(total_spent * 0.01, 2)  # 1% cashback
                })

            # Get top 5 transactions
            if "Сумма_операции" in df_filtered.columns:
                top_transactions = df_filtered.nlargest(5, "Сумма_операции")
                response["top_transactions"] = [{
                    "date": row["Дата_операции"].strftime("%d.%m.%Y"),
                    "amount": row["Сумма_операции"],
                    "category": row.get("Категория", ""),
                    "description": row.get("Описание", "")
                } for _, row in top_transactions.iterrows()]

        return response

    except ValueError as e:
        logger.error(f"Invalid date format in home_page: {e}")
        raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
    except Exception as e:
        logger.error(f"Error in home_page: {e}")
        raise


def events_page(date_str: str, date_range: str = "M") -> Dict[str, Any]:
    """Generate data for events page."""
    try:
        # Load and filter transactions
        df = load_transactions()
        df_filtered = filter_transactions_by_date(df, date_str, date_range)

        response = {
            "period": date_range,
            "expenses": {
                "total": 0,
                "by_category": []
            },
            "income": {
                "total": 0,
                "by_category": []
            },
            "currency_rates": fetch_currency_rates(["USD", "EUR"]),
            "stock_prices": fetch_stock_prices(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
        }

        if not df_filtered.empty:
            # Process expenses (positive amounts)
            if "Сумма_операции" in df_filtered.columns:
                expenses = df_filtered[df_filtered["Сумма_операции"] > 0]
                if not expenses.empty:
                    response["expenses"]["total"] = round(expenses["Сумма_операции"].sum(), 2)
                    if "Категория" in expenses.columns:
                        by_category = expenses.groupby("Категория")["Сумма_операции"].sum()
                        response["expenses"]["by_category"] = [
                            {"category": cat, "amount": round(amt, 2)}
                            for cat, amt in by_category.items()
                        ]

                # Process income (negative amounts)
                income = df_filtered[df_filtered["Сумма_операции"] < 0]
                if not income.empty:
                    response["income"]["total"] = round(abs(income["Сумма_операции"].sum()), 2)
                    if "Категория" in income.columns:
                        by_category = income.groupby("Категория")["Сумма_операции"].sum()
                        response["income"]["by_category"] = [
                            {"category": cat, "amount": round(abs(amt), 2)}
                            for cat, amt in by_category.items()
                        ]

        return response

    except ValueError as e:
        logger.error(f"Invalid date format in events_page: {e}")
        raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
    except Exception as e:
        logger.error(f"Error in events_page: {e}")
        raise


def search_transactions_by_description(transactions: List[Dict], search_str: str) -> List[Dict]:
    """
    Ищет транзакции по заданной строке в описании с использованием регулярных выражений.

    Args:
        transactions: Список словарей с транзакциями
        search_str: Строка для поиска в описании

    Returns:
        Список транзакций, где описание содержит искомую строку
    """
    pattern = re.compile(search_str, re.IGNORECASE)
    return [t for t in transactions if 'description' in t and pattern.search(t['description'])]


def count_transactions_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством операций по каждой категории
    """
    category_counter = Counter()
    for t in transactions:
        if 'description' in t and t['description'] in categories:
            category_counter[t['description']] += 1
    return dict(category_counter)
