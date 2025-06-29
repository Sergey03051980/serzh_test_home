import pytest
from unittest.mock import patch
from datetime import datetime
from flask import Flask, template_rendered
from src.analysis_bank.views import (
    home_page,
    events_page,
    get_currency_rates,
    get_greeting
)


# Фикстура для тестового приложения
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Регистрируем маршруты
    app.add_url_rule('/', view_func=home_page)
    app.add_url_rule('/events', view_func=events_page)

    return app


# Фикстура для тестового клиента
@pytest.fixture
def client(app):
    return app.test_client()


# Фикстура для перехвата рендеринга шаблонов
@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


# Тест для get_currency_rates (успешный случай)
@patch('requests.get')
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {'rates': {'USD': 75.0}}
    result = get_currency_rates(['USD'])
    assert result == [{"currency": "USD", "rate": 75.0}]
    mock_get.assert_called_once()


# Тест для ошибки API (исправленный)
@patch('requests.get')
def test_get_currency_rates_api_error(mock_get):
    mock_get.side_effect = Exception("API Error")
    result = get_currency_rates(['USD'])
    # Ожидаем структуру с ошибкой, а не пустой список
    assert result == [{"currency": "USD", "rate": 0, "error": "API Error"}]


from unittest.mock import patch, MagicMock

@patch('src.analysis_bank.views.render_template')
def test_home_page(mock_render):
    mock_render.return_value = "home page content"
    from src.analysis_bank.views import home_page
    result = home_page()
    mock_render.assert_called_once_with('index.html', title='Home')
    assert result == "home page content"

@patch('src.analysis_bank.views.render_template')
def test_events_page(mock_render):
    mock_render.return_value = "events page content"
    from src.analysis_bank.views import events_page
    result = events_page()
    mock_render.assert_called_once_with('events.html', title='Events')
    assert result == "events page content"


# Тест для get_greeting
def test_get_greeting():
    morning = datetime(2023, 1, 1, 8, 0, 0)
    assert get_greeting(morning) == "Доброе утро"

    afternoon = datetime(2023, 1, 1, 14, 0, 0)
    assert get_greeting(afternoon) == "Добрый день"

    evening = datetime(2023, 1, 1, 19, 0, 0)
    assert get_greeting(evening) == "Добрый вечер"

    night = datetime(2023, 1, 1, 2, 0, 0)
    assert get_greeting(night) == "Доброй ночи"

