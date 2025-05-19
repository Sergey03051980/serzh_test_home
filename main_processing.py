from src.pythonproject.processing import filter_by_state, sort_by_date

sample_data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

if __name__ == "__main__":
    print("=== Фильтрация операций ===")
    print("EXECUTED операции:", [op['id'] for op in filter_by_state(sample_data)])
    print("CANCELED операции:", [op['id'] for op in filter_by_state(sample_data, 'CANCELED')])

    print("\n=== Сортировка операций ===")
    print("По убыванию даты:", [op['id'] for op in sort_by_date(sample_data)])
    print("По возрастанию даты:", [op['id'] for op in sort_by_date(sample_data, False)])
