import logging
from datetime import datetime
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names by replacing spaces with underscores"""
    if not df.empty:
        df.columns = [col.replace(" ", "_") for col in df.columns]
    return df


def home_page(date_str: str) -> Dict[str, Any]:
    """Generate data for home page."""
    try:
        # This will be mocked in tests
        df = load_transactions()
        df = normalize_column_names(df)

        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        response = {
            "greeting": get_greeting(datetime.now()),
            "cards": [],
            "top_transactions": []
        }

        if not df.empty:
            # Process cards
            if "Номер_карты" in df.columns:
                for card in df["Номер_карты"].unique():
                    card_df = df[df["Номер_карты"] == card]
                    total = card_df["Сумма_операции"].sum()
                    response["cards"].append({
                        "last_digits": str(card)[-4:],
                        "total_spent": round(total, 2),
                        "cashback": round(total * 0.01, 2)
                    })

            # Process top transactions
            if "Сумма_операции" in df.columns:
                top_trans = df.nlargest(5, "Сумма_операции")
                response["top_transactions"] = [{
                    "date": row["Дата_операции"].strftime("%d.%m.%Y"),
                    "amount": row["Сумма_операции"],
                    "category": row.get("Категория", ""),
                    "description": row.get("Описание", "")
                } for _, row in top_trans.iterrows()]

        return response

    except ValueError as e:
        logger.error(f"Invalid date format: {e}")
        raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'")
    except Exception as e:
        logger.error(f"Error in home_page: {e}")
        raise


def events_page(date_str: str, date_range: str = "M") -> Dict[str, Any]:
    """Generate data for events page."""
    try:
        df = load_transactions()
        df = normalize_column_names(df)

        # Validate inputs
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        if date_range not in ["W", "M", "Y", "ALL"]:
            raise ValueError("Invalid date range")

        response = {
            "period": date_range,
            "expenses": {"total": 0, "by_category": []},
            "income": {"total": 0, "by_category": []}
        }

        if not df.empty and "Сумма_операции" in df.columns:
            # Process expenses
            expenses = df[df["Сумма_операции"] > 0]
            if not expenses.empty:
                response["expenses"]["total"] = round(expenses["Сумма_операции"].sum(), 2)
                if "Категория" in expenses.columns:
                    by_cat = expenses.groupby("Категория")["Сумма_операции"].sum()
                    response["expenses"]["by_category"] = [
                        {"category": k, "amount": round(v, 2)}
                        for k, v in by_cat.items()
                    ]

            # Process income
            income = df[df["Сумма_операции"] < 0]
            if not income.empty:
                response["income"]["total"] = round(abs(income["Сумма_операции"].sum()), 2)
                if "Категория" in income.columns:
                    by_cat = income.groupby("Категория")["Сумма_операции"].sum()
                    response["income"]["by_category"] = [
                        {"category": k, "amount": round(abs(v), 2)}
                        for k, v in by_cat.items()
                    ]

        return response

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in events_page: {e}")
        raise


def load_transactions():
    """This will be mocked in tests"""
    return pd.DataFrame()


def get_greeting(time: datetime) -> str:
    """Get time-appropriate greeting."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"
