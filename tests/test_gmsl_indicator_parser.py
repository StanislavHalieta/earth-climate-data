import pytest
import math
from app.api.nasa.gmsl_indicator.gmsl_indicator_parser import format_gmsl_indicator_data

# Готуємо стабільний набір даних (рівномірний підйом рівня моря)
GOOD_DATA_LIST = [
    {"decimal_year": 2020.0, "gmsl": 10.0, "date": "01-01-2020"},
    {"decimal_year": 2021.0, "gmsl": 10.3, "date": "01-01-2021"},
    {"decimal_year": 2022.0, "gmsl": 10.6, "date": "01-01-2022"},
    {"decimal_year": 2023.0, "gmsl": 11.0, "date": "01-01-2023"},
]

# Готуємо занадто короткий список даних
SHORT_DATA_LIST = [
    {"decimal_year": 2023.0, "gmsl": 11.0, "date": "01-01-2023"}
]


def test_format_gmsl_indicator_data_success():
    """1. Тест успішного розрахунку кліматичних індексів для стабільних даних"""
    result = format_gmsl_indicator_data(GOOD_DATA_LIST)
    
    # Перевіряємо базові поля
    assert result["date"] == "01-01-2023"
    assert result["model"] == "QUANTUM_MOMENTUM_V17"
    assert result["compatibility_protocol"] == "GENOMIC_DATA_INTEGRATION"
    
    # Математика: h_first = 10.0 * 10 = 100.0, h_last = 11.0 * 10 = 110.0
    # observed_rise = 110.0 - 100.0 = 10.0
    assert result["observed_rise_mm"] == pytest.approx(10.0)
    
    # Перевіряємо структуру вкладених коефіцієнтів
    coeffs = result["multi_source_coefficients"]
    assert "v_recent_mm_yr" in coeffs
    assert "v_total_mm_yr" in coeffs
    assert coeffs["potential_energy_debt"] == "STABLE"


def test_format_gmsl_indicator_data_insufficiency():
    """2. Тест захисту від недостатньої кількості даних (менше 2 записів)"""
    result = format_gmsl_indicator_data(SHORT_DATA_LIST)
    
    assert "error" in result
    assert result["error"] == "Critical data insufficiency"


def test_format_gmsl_indicator_data_negative_velocity():
    """3. Тест логіки 'пружини' (+20% до небезпеки) при від'ємній швидкості"""
    # Створюємо дані, де рівень моря спочатку піднявся, а в кінці різко впав
    negative_trend_data = [
        {"decimal_year": 2020.0, "gmsl": 10.0, "date": "01-01-2020"},
        {"decimal_year": 2021.0, "gmsl": 12.0, "date": "01-01-2021"},
        {"decimal_year": 2022.0, "gmsl": 13.0, "date": "01-01-2022"},
        {"decimal_year": 2023.0, "gmsl": 11.0, "date": "01-01-2023"}, # впав з 13 до 11
    ]
    
    result = format_gmsl_indicator_data(negative_trend_data)
    coeffs = result["multi_source_coefficients"]
    
    # Оскільки рівень впав, але загальний підйом за 3 роки є позитивним (>50 мм немає, бо підйом 10 мм)
    # Перевіряємо, чи індекс небезпеки залишається активним і більшим за мінімальний поріг
    assert result["hazard_index"] >= 0.015