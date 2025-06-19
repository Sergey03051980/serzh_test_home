import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import pandas as pd
from datetime import datetime
from analysis_bank.views import home_page, events_page


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'Номер карты': ['1234567890123456', '9876543210987654'],
        'Сумма_операции': [100.5, 5000.0],
        'Дата_операции': [datetime(2023, 5, 1), datetime(2023, 5, 2)],
        'Категория': ['Магазин', 'Перевод'],
        'Описание': ['Покупка в магазине', 'Перевод другу']
    })


def test_home_page_structure(sample_dataframe, mocker):
    mocker.patch("src.utils.load_transactions", return_value=sample_dataframe, create=True)
    result = home_page("2023-05-01 12:00:00")
    assert isinstance(result, dict)


def test_events_page_structure(sample_dataframe, mocker):
    mocker.patch("src.utils.load_transactions", return_value=sample_dataframe, create=True)
    result = events_page("2023-05-01 12:00:00", "M")
    assert isinstance(result, dict)


def test_home_page_with_invalid_date(sample_dataframe, mocker):
    mocker.patch("analysis_bank.utils.load_transactions", return_value=sample_dataframe)
    with pytest.raises(ValueError):
        home_page("invalid-date")
