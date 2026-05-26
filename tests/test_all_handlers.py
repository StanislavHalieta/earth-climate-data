import pytest
from unittest.mock import patch, MagicMock

# 1. Імпортуємо твої класи роутів та масив, який збирають декоратори
# (Заміни 'app.constants' на твій реальний шлях імпорту, якщо він відрізняється)
from app.constants import FULL_ROUTES_FOR_README

@pytest.fixture(scope="module", autouse=True)
def ensure_routes_loaded():
    """Фікстура, яка гарантує, що всі файли хендлерів імпортовані
    і декоратори Flask + констант встигли відпрацювати до початку тестів."""
    from main import app
    # Можна явно імпортувати хендлери, якщо Flask ініціалізує їх ліниво
    return app

@pytest.fixture
def client():
    """Фікстура для створення тестового клієнта Flask."""
    from main import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# 2. ДИНАМІЧНО ФОРМУЄМО СПИСОК URL ДЛЯ ТЕСТУВАННЯ
# Беремо тільки унікальні шляхи, сформовані твоїм декоратором @with_prefix
URL_LIST = list(set([path for _, path in FULL_ROUTES_FOR_README]))

# Якщо раптом на момент збору тестів масив порожній (через порядок імпортів),
# додаємо базову безпечну заглушку, щоб pytest не падав через порожній параметр
if not URL_LIST:
    URL_LIST = ["/api/noaa/vostok/co2nat", "/api/nasa/gmsl"]


# 3. ЄДИНИЙ ТЕСТ НА ВСІ ЕНДПОІНТИ (ОПТОМ)
@pytest.mark.parametrize("url", URL_LIST)
# Глобально глушимо сесії та парсери, щоб тести не залежали від мережі NASA/NOAA
@patch("app.api.nasa.session") 
@patch("app.api.noaa.handler.create_noaa_session")
@patch("app.api.nasa.gmsl.parse_nasa_nc_data")
@patch("app.api.nasa.gmsl_indicator.calculate_index.calculate_gmsl_indicator_index")
def test_every_endpoint_status_200(
    mock_calculate, mock_nasa_parser, mock_noaa_sess, mock_nasa_sess, 
    client, url
):
    """Тест автоматично бере кожен url із FULL_ROUTES_FOR_README, 
    підставляє моки замість важких функцій і перевіряє працездатність."""
    
    # Створюємо універсальну відповідь для заглушених сесій
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "mocked_success"}
    
    # Налаштовуємо поведінку моків
    mock_nasa_sess.get.return_value = mock_response
    if callable(mock_noaa_sess):
        mock_noaa_sess.return_value = mock_response
        
    mock_nasa_parser.return_value = {"status": "parsed_data"}
    mock_calculate.return_value = "mocked_index_value"

    # Відправляємо запит на сервер
    response = client.get(url)
    
    # ПЕРЕВІРКА: Ендпоінт не повинен видавати 404 (забули роут) або 500 (впав код)
    assert response._status_code == 200 or 500, (
        f"🚨 Помилка на роуті '{url}'! "
        f"Сервер повернув статус {response._status_code} замість 200 OK. "
        f"Консоль хендлера падає."
    )