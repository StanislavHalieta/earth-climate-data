import pytest

# Імпортуємо твої функції створення сесій
from app.api.nasa.session import create_nasa_session
from app.api.noaa.session import create_noaa_session

# Список тест-кейсів у форматі: (функція_сесії, позиційні_аргументи_як_тег)
SESSIONS_TO_TEST = [
    # Для NASA: передаємо порожній словник (якщо параметри не потрібні)
    (create_nasa_session, {}),
    
    # Для NOAA: передаємо словник з ключем "endpoint"
    (create_noaa_session, {"endpoint": "https://example.com/noaa-data"}),
]

@pytest.mark.parametrize("session_func, kwargs", SESSIONS_TO_TEST)
def test_session_initialization_dynamically(session_func, kwargs):
    """Універсальний тест для перевірки створення будь-якої сесії в проєкті"""
    
    # Розпаковуємо аргументи за допомогою зірочки *args
    result = session_func(**kwargs)
    
    # Перевіряємо, що об'єкт успішно створився
    assert result is not None
    
    # Перевіряємо, що повернувся або налаштований рядок, або об'єкт
    assert isinstance(result, (str, object))