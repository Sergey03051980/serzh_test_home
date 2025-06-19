from src.analysis_bank.services import (
    find_phone_transactions,
    investment_bank,
    profitable_cashback_categories,
    find_person_transfers
)


def test_profitable_cashback_categories():
    """Test profitable_cashback_categories calculation."""
    sample_transactions = [
        {
            "Дата_операции": "2023-05-01",
            "Категория": "Супермаркеты",
            "Кешбэк": 1.0,
            "Описание": "Покупка в магазине"
        },
        {
            "Дата_операции": "2023-04-30",  # Не должна учитываться
            "Категория": "Рестораны",
            "Кешбэк": 5.0
        }
    ]
    result = profitable_cashback_categories(sample_transactions, 2023, 5)
    assert isinstance(result, dict)
    assert "Супермаркеты" in result
    assert result["Супермаркеты"] == 1.0


def test_investment_bank():
    """Test investment_bank calculation."""
    sample_transactions = [
        {
            "Дата_операции": "2023-05-15",
            "Сумма_операции": "123.45",  # Округлится до 150 (при limit=50)
            "Описание": "Покупка"
        },
        {
            "Дата_операции": "2023-05-20",
            "Сумма_операции": "178.90",  # Округлится до 200
            "Описание": "Покупка"
        }
    ]
    result = investment_bank("2023-05", sample_transactions, 50)
    assert isinstance(result, float)
    assert result > 0
    # 150-123.45 + 200-178.90 = 47.65
    assert result == 47.65


def test_find_phone_transactions(phone_transactions):
    """Test find_phone_transactions functionality."""
    result = find_phone_transactions(phone_transactions)
    assert isinstance(result, list)
    assert len(result) == 1
    assert "Мобильная связь" in result[0]["Категория"]


def test_find_person_transfers():
    """Test find_person_transfers functionality."""
    transactions = [
        {
            "Дата_операции": "2023-01-01",
            "Отправитель": "Иванов И.",
            "Получатель": "Петров П.",
            "Сумма_операции": "100",
            "Категория": "Перевод",
            "Описание": "Перевод денег"
        },
        {
            "Дата_операции": "2023-01-02",
            "Отправитель": "Петров П.",
            "Получатель": "Сидоров С.",
            "Сумма_операции": "200",
            "Категория": "Перевод",
            "Описание": "Оплата услуг"
        },
    ]

    # Тест входящих переводов
    result = find_person_transfers(transactions, "Петров П.")
    assert len(result) == 1
    assert result[0]["Отправитель"] == "Иванов И."

    # Тест исходящих переводов
    result = find_person_transfers(transactions, "Петров П.", is_sender=True)
    assert len(result) == 1
    assert result[0]["Получатель"] == "Сидоров С."
