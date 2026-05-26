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
    assert result["type"] == "paleo_stations"
    assert "data" in result
    
    data_list = result["data"]
    # Має бути 2 записи, бо третій запис (60.0 ka) відсікається фільтром [<= 50]
    assert len(data_list) == 2
    
    # Перевіряємо перший запис (0 тисяч років тому)
    # Математика року: 2026 - (0.0 * 1000) = 2026
    first_row = data_list[0]
    assert first_row["year"] == 2026
    assert first_row["age_ka"] == pytest.approx(0.0)
    assert first_row["sea_level"] == pytest.approx(0.0)
    
    # Перевіряємо другий запис (20 тисяч років тому)
    # Математика року: 2026 - (20.0 * 1000) = -17974 (до нашої ери)
    second_row = data_list[1]
    assert second_row["year"] == -17974
    assert second_row["sea_level"] == pytest.approx(-120.0)

def test_parse_noaa_paleo_sea_level_data_wrong_input():
    """2. Тест захисту від помилкових відповідей сервера (якщо прийшов dict замість тексту)"""
    fake_error_dict = {"status": "500", "message": "Internal NASA Error"}
    result = parse_noaa_paleo_sea_level_data(fake_error_dict)
    
    assert result.get("status") == "error"
    assert "HTTP request failed" in result["message"]