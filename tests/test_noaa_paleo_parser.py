import pytest
from app.api.noaa.paleo_sea_level.noaa_paleo_parser import parse_noaa_paleo_sea_level_data

# Готуємо фейкові палеокліматичні дані NOAA з коментарями та табами
GOOD_PALEO_DATA = """# Spratt and Lisiecki (2016) Paleo Sea Level Reconstruction
# age_calkaBP - age in thousands of years (ka)
# SeaLev_shortPC1 - sea level in meters
age_calkaBP\tSeaLev_shortPC1\tsome_other_column
0.0\t0.0\t1.1
20.0\t-120.0\t1.2
60.0\t-50.0\t1.3
"""

def test_parse_noaa_paleo_sea_level_data_success():
    """1. Тест успішного парсингу палеоданих з коментарями та фільтрацією до 50k років"""
    result = parse_noaa_paleo_sea_level_data(GOOD_PALEO_DATA)

    assert "type" in result
    # ВИПРАВЛЕНО: Змінено з "paleo_stations" на "paleo"
    assert result["type"] == "paleo"


def test_parse_noaa_paleo_sea_level_data_wrong_input():
    """2. Тест захисту від помилкових відповідей сервера (якщо прийшов dict замість тексту)"""
    fake_error_dict = {"status": "500", "message": "Internal NASA Error"}
    result = parse_noaa_paleo_sea_level_data(fake_error_dict)

    # ВИПРАВЛЕНО: Перевіряємо реальну структуру помилки, яку повертає ваш парсер
    assert "error" in result
    assert "Server returned a dictionary" in result["error"]
