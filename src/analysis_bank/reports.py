import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import json
import logging


def report_decorator(filename=None):
    """Декоратор для сохранения отчетов в файл."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            fname = filename if filename else f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d')}.json"
            with open(fname, 'w') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца."""
    end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]

    return {
        "category": category,
        "total": float(filtered['Сумма операции'].sum()),
        "by_month": filtered.groupby(filtered['Дата операции'].dt.to_period('M'))['Сумма операции'].sum().to_dict()
    }


@report_decorator()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """Средние траты по дням недели."""
    end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]

    return filtered.groupby(filtered['Дата операции'].dt.day_name())['Сумма операции'].mean().to_dict()


@report_decorator()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """Средние траты в рабочие/выходные дни."""
    end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ].copy()

    filtered['is_weekend'] = filtered['Дата операции'].dt.dayofweek >= 5
    return filtered.groupby('is_weekend')['Сумма операции'].mean().to_dict()
