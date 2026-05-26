import pytest

from app.api.noaa.noaa_ice_extent.noaa_ice_data_parser import parse_noaa_ice_data

# Готуємо правильний шматочок CSV у форматі NOAA
GOOD_NOAA_CSV = """Source Data: NSIDC Sea Ice Index
Year, Month, Day, Extent, Missing, Source_Data
2023, 10, 24, 4.56, 0.0, 'N_seaice'
2023, 10, 25, 4.61, 0.0, 'N_seaice'
"""

# Готуємо неправильний текст (наприклад, HTML сторінка помилки)
BAD_HTML_RESPONSE = "<html><body><h1>403 Forbidden</h1></body></html>"


def test_parse_noaa_ice_data_success():
    """1. Тест успішного парсингу правильної таблиці NOAA"""
    result = parse_noaa_ice_data(GOOD_NOAA_CSV)
    
    assert result["status"] == "success"
    assert "data" in result
    
    # Очікуємо 2 записи в результаті
    data_list = result["data"]
    assert len(data_list) == 2
    
    # Перевіряємо перший рядок (Pandas має склеїти 2023, 10, 24 у правильну дату)
    first_row = data_list[0]
    assert first_row["date"] == "2023-10-24"
    assert first_row["Extent"] == pytest.approx(4.56)
    assert first_row["Missing"] == pytest.approx(0.0)


def test_parse_noaa_ice_data_wrong_type():
    """2. Тест захисту від неправильного типу даних (наприклад, None або число)"""
    result = parse_noaa_ice_data(None)
    
    assert result["status"] == "error"
    assert "Очікувався рядок (str)" in result["message"]


def test_parse_noaa_ice_data_not_csv():
    """3. Тест захисту від тексту, який не містить ключового слова 'Year'"""
    result = parse_noaa_ice_data(BAD_HTML_RESPONSE)
    
    assert result["status"] == "error"
    assert "не схожі на формат NOAA CSV" in result["message"]