import pandas as pd
from typing import Dict, Optional
from datetime import datetime
import json
import logging


# Сначала определяем декоратор
def report_decorator(filename=None):
    """Декоратор для сохранения отчетов в файл."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            fname = filename if filename else f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d')}.json"
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logging.error(f"Error saving report to {fname}: {e}")
            return result

        return wrapper

    return decorator


# Затем определяем функции, которые используют декоратор
@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Траты по категории за последние 3 месяца."""
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions['Категория'].str.contains(category, case=False)) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ]

    by_month = filtered.groupby(filtered['Дата операции'].dt.strftime('%Y-%m'))['Сумма операции'].sum()

    return {
        "category": category,
        "total": float(filtered['Сумма операции'].sum()),
        "by_month": by_month.to_dict()
    }


@report_decorator()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> Dict[str, float]:
    """Средние траты по дням недели."""
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
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
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    end_date = pd.to_datetime(date) if date else pd.to_datetime(datetime.now())
    start_date = end_date - pd.DateOffset(months=3)

    filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ].copy()

    filtered['is_weekend'] = filtered['Дата операции'].dt.dayofweek >= 5
    return filtered.groupby('is_weekend')['Сумма операции'].mean().to_dict()


# Добавляем точку входа для тестирования
if __name__ == "__main__":
    # Пример использования
    test_data = pd.DataFrame({
        'Дата операции': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Сумма операции': [1000, 500, 800],
        'Статус': ['OK', 'OK', 'OK']
    })

    print(spending_by_category(test_data, "Еда"))
    print(spending_by_weekday(test_data))
    print(spending_by_workday(test_data))
