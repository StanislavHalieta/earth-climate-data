import pytest
from app.helpers.date_parsers import decimal_to_date, index_to_date

# ==========================================
# ТЕСТИ ДЛЯ decimal_to_date
# ==========================================

def test_decimal_to_date_start_of_year():
    """1. Тест першого дня звичайного року (1 січня)"""
    assert decimal_to_date(2023.0) == "01-01-2023"


def test_decimal_to_date_leap_year_february():
    """2. Тест кінця лютого у високосному році (2024)"""
    # Перевіряємо, що додавання дробової частини повертає лютий 2024 року
    result = decimal_to_date(2024 + (59 / 366))
    assert result.endswith("-02-2024")


def test_decimal_to_date_half_year():
    """3. Тест середини року (початок липня)"""
    assert decimal_to_date(2023.5).endswith("-07-2023")


# ==========================================
# ТЕСТИ ДЛЯ index_to_date
# ==========================================

def test_index_to_date_zero():
    """4. Тест базової дати NASA (0 днів від 1 січня 1992)"""
    assert index_to_date(0) == "01-01-1992"


def test_index_to_date_one_year():
    """5. Тест через 366 днів (1992 — високосний, тому 1 січня 1993)"""
    assert index_to_date(366) == "01-01-1993"


def test_index_to_date_random_day():
    """6. Тест через 10000 днів від базової дати"""
    assert index_to_date(10000) == "19-05-2019"