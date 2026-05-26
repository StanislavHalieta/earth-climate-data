import os
import tempfile
import pytest
import netCDF4
import numpy as np
from app.api.nasa.gmsl.nc_nasa_parser import parse_nasa_nc_data

def create_fake_nc_bytes():
    """Створює тимчасовий NetCDF4 файл на диску, зчитує його в байти та видаляє"""
    # Створюємо тимчасовий файл у безпечній папці ОС
    with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Відкриваємо та записуємо звичайний NetCDF4 файл на диск
        with netCDF4.Dataset(tmp_path, mode="w", format="NETCDF4") as ds:
            ds.createDimension("time", 3)
            
            time_var = ds.createVariable("time", "f4", ("time",))
            gmsl_var = ds.createVariable("global_average_sea_level_change", "f4", ("time",))
            ais_var = ds.createVariable("AIS_mean", "f4", ("time",))
            gris_var = ds.createVariable("GrIS_mean", "f4", ("time",))
            
            time_var[:] = np.array([2023.0, 2023.5, 2024.0], dtype=np.float32)
            gmsl_var[:] = np.array([3.1, np.nan, 3.8], dtype=np.float32)
            ais_var[:] = np.array([0.5, 0.6, 0.7], dtype=np.float32)
            gris_var[:] = np.array([0.2, 0.3, 0.4], dtype=np.float32)

        # Тепер зчитуємо цей файл назад у вигляді чистих бінарних байтів
        with open(tmp_path, "rb") as f:
            binary_content = f.read()
            
        return binary_content

    finally:
        # Гарантовано видаляємо тимчасовий файл із диска після зчитування
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_parse_nasa_nc_data_success():
    """1. Тест успішного парсингу валідного бінарного NetCDF файлу"""
    binary_content = create_fake_nc_bytes()
    
    result = parse_nasa_nc_data(binary_content)
    
    assert isinstance(result, list)
    assert len(result) == 3
    
    first_row = result[0]
    assert first_row["date_index"] == pytest.approx(2023.0)
    assert first_row["total_change"] == pytest.approx(3.1)
    assert first_row["ice_sheets"] == pytest.approx(0.7)
    
    second_row = result[1]
    assert second_row["total_change"] == pytest.approx(0.0)


def test_parse_nasa_nc_data_failure():
    """2. Тест поведінки парсера при пошкоджених або невалідних бінарних даних"""
    bad_binary_content = b"completely_broken_and_corrupted_binary_data"
    
    result = parse_nasa_nc_data(bad_binary_content)
    
    assert isinstance(result, dict)
    assert "error" in result
    assert "Failed to parse .nc file" in result["error"]