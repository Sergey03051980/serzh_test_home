from pathlib import Path
from typing import Any, List, Dict

import pandas as pd

from analysis_bank.models import Transaction
from utils import load_transactions, search_transactions_by_description, count_transactions_by_category


def prepare_transactions(raw_data: List[Dict[str, Any]]) -> List[Transaction]:
    return [
        Transaction(
            Дата_операции=str(item.get('Дата_операции', '')),
            Категория=str(item.get('Категория', '')),
            Описание=str(item.get('Описание', '')),
            Сумма_операции=str(item.get('Сумма_операции', '0')),
            Кешбэк=float(item.get('Кешбэк', 0)),
            Отправитель=str(item.get('Отправитель', '')),
            Получатель=str(item.get('Получатель', ''))
        )
        for item in raw_data
    ]


def get_file_path(choice):
    """Возвращает путь к файлу на основе выбора пользователя"""
    base_dir = Path(__file__).parent.parent
    files = {
        '1': 'transactions.json',
        '2': 'transactions.csv',
        '3': 'transactions.xlsx'
    }
    filename = files.get(choice)
    if not filename:
        raise ValueError("Некорректный выбор файла")
    return base_dir / 'data' / filename


def create_sample_file(file_path):
    """Создает тестовый файл с транзакциями"""
    file_path.parent.mkdir(exist_ok=True)

    sample_data = {
        'Дата': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'Сумма': [1500.00, 2500.50, 980.75],
        'Категория': ['Еда', 'Транспорт', 'Развлечения'],
        'Описание': ['Продукты', 'Такси', 'Кинотеатр']
    }
    df = pd.DataFrame(sample_data)

    if file_path.suffix == '.json':
        df.to_json(file_path, orient='records', indent=2, force_ascii=False)
    elif file_path.suffix == '.csv':
        df.to_csv(file_path, index=False, encoding='utf-8')
    elif file_path.suffix == '.xlsx':
        df.to_excel(file_path, index=False)


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        print("\nГлавное меню:")
        print("1. Работа с JSON-файлом")
        print("2. Работа с CSV-файлом")
        print("3. Работа с XLSX-файлом")
        print("4. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == '4':
            print("До свидания!")
            break

        try:
            file_path = get_file_path(choice)

            if not file_path.exists():
                print(f"\nФайл {file_path.name} не найден!")
                create_sample_file(file_path)
                print(f"Создан тестовый файл: {file_path}")

            try:
                transactions = load_transactions(str(file_path))
                print("\nДанные успешно загружены!")
                print(transactions.head())

                # Здесь можно добавить анализ данных

            except Exception as load_error:
                print(f"\nОшибка при загрузке файла: {load_error}")

        except ValueError as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nНеожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
