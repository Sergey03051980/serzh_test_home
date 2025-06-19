import functools
import json
import logging
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def report_decorator(filename: Optional[str] = None) -> Callable:
    """Decorator to save report results to file.

    Args:
        filename: Optional filename to save report

    Returns:
        Decorator function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            # Determine filename
            report_filename = filename or f"{func.__name__}_report.json"

            # Save to file
            try:
                with open(report_filename, "w") as f:
                    if isinstance(result, pd.DataFrame):
                        json.dump(result.to_dict(orient="records"), f)
                    else:
                        json.dump(result, f)
                logger.info(f"Report saved to {report_filename}")
            except Exception as e:
                logger.error(f"Error saving report: {e}")

            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, start_date):
    if not pd.api.types.is_datetime64_any_dtype(transactions["Дата_операции"]):
        """Calculate spending by category since a given date."""
        # Преобразуем даты в datetime
        transactions = transactions.copy()  # Чтобы избежать SettingWithCopyWarning
        transactions["Дата_операции"] = pd.to_datetime(transactions["Дата_операции"])
        start_date = pd.to_datetime(start_date)

    # Фильтруем данные
    mask = (
            (transactions["Дата_операции"] >= start_date) &
            (transactions["Описание"].str.contains(category, case=False))
    )
    filtered = transactions[mask]

    return filtered["Сумма"].sum()


@report_decorator()
def spending_by_weekday(transactions, start_date):
    transactions = transactions.copy()
    transactions["Дата_операции"] = pd.to_datetime(transactions["Дата_операции"])
    start_date = pd.to_datetime(start_date)

    filtered = transactions[transactions["Дата_операции"] >= start_date]

    # Создаем все возможные дни недели
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    filtered["День_недели"] = filtered["Дата_операции"].dt.day_name()

    # Группируем и добавляем отсутствующие дни
    result = filtered.groupby("День_недели", as_index=False)["Сумма"].sum()
    result = result.set_index("День_недели").reindex(weekdays).fillna(0).reset_index()

    return result


@report_decorator("workday_spending_report.json")
def spending_by_workday(transactions, start_date):
    transactions = transactions.copy()
    transactions["Дата_операции"] = pd.to_datetime(transactions["Дата_операции"])
    start_date = pd.to_datetime(start_date)

    filtered = transactions[transactions["Дата_операции"] >= start_date]
    filtered["Тип_дня"] = filtered["Дата_операции"].apply(
        lambda x: "Рабочий" if x.weekday() < 5 else "Выходной"
    )

    # Группируем и добавляем оба типа дней
    result = filtered.groupby("Тип_дня", as_index=False)["Сумма"].sum()
    if len(result) < 2:
        types = ["Рабочий", "Выходной"]
        result = result.set_index("Тип_дня").reindex(types).fillna(0).reset_index()

    return result
