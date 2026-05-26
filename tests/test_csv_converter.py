import pytest
from app.helpers.csv_converter import parse_dap_csv

# Готуємо правильний шматочок фейкового OPeNDAP CSV файлу
GOOD_DAP_DATA = """
/time, 2023.0, 2023.5, 2024.0
/global_average_sea_level_change, 3.1, 3.4, 3.8
/AIS_mean, 0.5, 0.6, 0.7
/GrIS_mean, 0.2, 0.3, 0.4
/global_average_thermosteric_sea_level_change_lower, 1.1, 1.2, 1.3
"""

# Готуємо зламаний шматочок (не вистачає даних в одній з колонок)
BAD_DAP_DATA = """
/time, 2023.0, 2023.5
/global_average_sea_level_change, 3.1
/AIS_mean, 0.5, 0.6
"""


def test_parse_dap_csv_success():
    """1. Тест успішного парсингу правильних CSV даних"""
    
    result = parse_dap_csv(GOOD_DAP_DATA)
    
    # Очікуємо 3 об'єкти в результаті, бо у нас 3 мітки часу (time)
    assert len(result) == 3
    
    # Перевіряємо перший запис
    first_row = result[0]
    assert first_row["date_index"] == 2023.0
    assert first_row["total_change"] == 3.1
    
    # Математика: ice_sheets = AIS_mean (0.5) + GrIS_mean (0.2) = 0.7
    assert first_row["ice_sheets"] == 0.7
    assert first_row["thermosteric"] == 1.1


def test_parse_dap_csv_empty_input():
    """2. Тест ситуації, коли прийшов порожній рядок"""
    result = parse_dap_csv("")
    assert result == []


def test_parse_dap_csv_robustness():
    """3. Тест на стійкість до битих даних (захист від IndexError/KeyError)"""
    # Ми передаємо ламані дані. Замість падіння всього сервера, 
    # функція має або пропустити биті рядки, або видати безпечну помилку
    try:
        result = parse_dap_csv(BAD_DAP_DATA)
        assert isinstance(result, list)
    except Exception as err:
        pytest.fail(f"Функція впала з помилкою {type(err).__name__}! Код треба захистити.")