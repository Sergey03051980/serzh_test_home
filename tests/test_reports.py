import pandas as pd
import pytest

from src.analysis_bank.reports import (
    spending_by_category,
    spending_by_weekday,
    spending_by_workday
)


@pytest.fixture
def sample_dataframe():
    """Фикстура с тестовыми данными."""
    data = {
        'Дата операции': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-04-15', '2023-04-16'],
        'Категория': ['Еда', 'Транспорт', 'Payment', 'Payment', 'Еда'],
        'Сумма операции': [1000, 500, 2500.25, 2600.25, 800],
        'Статус': ['OK', 'OK', 'OK', 'OK', 'OK']
    }
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'])
    return df


def test_spending_by_category(sample_dataframe):
    result = spending_by_category(
        sample_dataframe,
        "Payment",
        "2023-05-01"  # Период: 2023-02-01 - 2023-05-01
    )

    assert isinstance(result, dict)
    assert result["category"] == "Payment"
    # Ожидаем только транзакцию от 2023-04-15 (2600.25)
    assert result["total"] == pytest.approx(2600.25)
    assert isinstance(result["by_month"], dict)
    assert len(result["by_month"]) == 1  # Должен быть только апрель


def test_spending_by_weekday(sample_dataframe):
    result = spending_by_weekday(sample_dataframe, "2023-04-30")

    assert isinstance(result, dict)
    assert len(result) > 0
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        if day in result:
            assert isinstance(result[day], float)


def test_spending_by_workday(sample_dataframe):
    result = spending_by_workday(sample_dataframe, "2023-04-30")

    assert isinstance(result, dict)
    assert len(result) >= 1
    assert any(k in result for k in [True, False])
    for k, v in result.items():
        assert isinstance(k, bool)
        assert isinstance(v, float)

def test_empty_spending_report():
    # Тестируем обработку пустых данных
    pass
