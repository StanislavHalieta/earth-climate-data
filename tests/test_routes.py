import pytest
from app.constants import FULL_ROUTES_FOR_README, NoaaRoutes, NasaRoutes, VostokRoutes

# 1. ДИНАМІЧНО СТВОРЮЄМО СЛОВНИК ОЧІКУВАНИХ ЗНАЧЕНЬ
# Твій декоратор @with_prefix збирає пари (НАЗВА, ПОВНИЙ_ШЛЯХ).
# Перетворимо цей масив у зручний словник для швидкого пошуку.
EXPECTED_ROUTES = dict(FULL_ROUTES_FOR_README)


# 2. АВТОМАТИЧНО ЗБИРАЄМО ВСІ ІСНУЮЧІ КОНСТАНТИ З КЛАСІВ
def get_all_actual_constants():
    """Збирає всі константи (ВЕЛИКИМИ ЛІТЕРАМИ) з усіх твоїх класів роутів."""
    actual_routes = {}
    
    # Перебираємо класи, які ми використовуємо
    for route_class in [NoaaRoutes, NasaRoutes, VostokRoutes]:
        for key, value in route_class.__dict__.items():
            # Нас цікавлять тільки константи великими літерами (ігноруємо системні речі)
            if key.isupper() and isinstance(value, str):
                # Оскільки EXPECTED_ROUTES зберігає повні шляхи, нам треба знати, 
                # який повний шлях відповідає цій константі.
                # Ми беремо його прямо з нашого автогенерованого словника.
                actual_routes[key] = EXPECTED_ROUTES.get(key)
                
    return actual_routes

ACTUAL_ROUTES_MAP = get_all_actual_constants()


# 3. УНІВЕРСАЛЬНИЙ ТЕСТ-РОБОТ
@pytest.mark.parametrize("route_name", ACTUAL_ROUTES_MAP.keys())
def test_constant_matches_generated_path(route_name):
    """Тест автоматично бере кожну константу, знаходить її згенерований 
    декоратором повний шлях і перевіряє, що він не порожній і сформований правильно."""
    
    full_path = ACTUAL_ROUTES_MAP[route_name]
    
    # Перевірка 1: Чи взагалі декоратор зміг обробити цю константу
    assert full_path is not None, f"🚨 Константа '{route_name}' не була оброблена декоратором @with_prefix!"
    
    # Перевірка 2: Чи шлях починається з базового /api
    assert full_path.startswith("/api"), f"🚨 Шлях для '{route_name}' ({full_path}) має неправильний префікс! Очікується /api..."
    
    # Перевірка 3: Чи немає випадкових подвійних слешів через склеювання (наприклад, //noaa)
    assert "//" not in full_path, f"🚨 Шлях для '{route_name}' містить подвійний слеш: '{full_path}'!"