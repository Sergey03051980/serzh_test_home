import pandas as pd

from src.analysis_bank.reports import (
    spending_by_category,
    spending_by_weekday,
    spending_by_workday
)


def test_spending_by_category(sample_dataframe):
    result = spending_by_category(
        sample_dataframe,
        "Payment",  # Ищем по части описания
        pd.to_datetime("2023-05-01")  # Явное указание типа даты
    )
    assert result == 5100.5


def test_spending_by_weekday(sample_dataframe):
    """Test spending_by_weekday report."""
    # Используем дату раньше, чем в тестовых данных
    result = spending_by_weekday(sample_dataframe, "2023-04-30")

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0  # Проверяем, что есть результаты
    # Дополнительные проверки по необходимости


def test_spending_by_workday(sample_dataframe):
    """Test spending_by_workday report."""
    # Используем дату раньше, чем в тестовых данных
    result = spending_by_workday(sample_dataframe, "2023-04-30")

    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0  # Проверяем, что есть результаты
