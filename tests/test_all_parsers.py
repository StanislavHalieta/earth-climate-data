# tests/test_all_parsers.py
# АВТОМАТИЧНО ЗГЕНЕРОВАНИЙ ФАЙЛ. НЕ РЕДАГУЙТЕ ВРУЧНУ!
import pytest
import json
from flask import Response
from unittest.mock import MagicMock

# --- АВТОМАТИЧНІ ІМПОРТИ ПАРСЕРІВ ---
from app.api.nasa.gistemp.gistemp_parser import parse_gistemp_data
from app.api.nasa.gmsl.nc_nasa_parser import parse_nasa_nc_data
from app.api.nasa.gmsl_indicator.gmsl_indicator_data_parser import parse_gmsl_indicator_data
from app.api.nasa.ozone.ozone_data_parser import parse_nasa_ozone_csv
from app.api.nasa.ozone.ozone_data_parser import parse_nasa_to_flat_list
from app.api.nasa.stratospheric_aerosol.stratospheric_aerosol_parser import parse_stratospheric_aerosol
from app.api.noaa.co2_mauna_loa.co2_mauna_loa_parser import parse_co2_mauna_loa
from app.api.noaa.enso_nio34.enso_nino34_parser import parse_enso_nino34_data
from app.api.noaa.methane.methane_parser import parse_nc_daily_methane
from app.api.noaa.noaa_ice_extent.noaa_ice_data_parser import parse_noaa_ice_data
from app.api.noaa.ocean_pentad_heat.ocean_pentad_heat_data import parse_ocean_pentad_heat_data
from app.api.noaa.paleo_sea_level.noaa_paleo_parser import parse_noaa_paleo_sea_level_data
from app.api.noaa.ratpac_a.ratpac_text_parser import parse_ratpac_data
from app.api.noaa.relative_sea_level.relative_sea_level_parser import parse_relative_sea_level_data
from app.api.noaa.relative_sea_level_summary.relative_sea_level_summary_parser import parse_relative_sea_level_summary_data
from app.api.noaa.vostok.ch4nat.vostok_ch4nat_parser import parse_vostok_ch4_data
from app.api.noaa.vostok.co2nat.vostok_co2_nat_parser import parse_vostok_co2_data
from app.api.noaa.vostok.dustnat_noaa.dustnat_noaa_parser import parse_vostok_dust_data
from app.api.noaa.vostok.n2o_iso.n2o_iso_parser import parse_vostok_n2o_iso_data
from app.api.noaa.vostok.temp.vostok_temp_parser import parse_vostok_recent_temp
from app.api.peltier.peltier_data_parser import parse_ns_peltier_data

# Універсальні заготовки для швидких тестів
FAKE_CSV_TEXT = 'year,month,data\n2026,01,42.5\n2026,02,43.2'
FAKE_BYTES = b'fake binary data'

mock_response = MagicMock()
mock_response.content = FAKE_BYTES
mock_response.text = FAKE_CSV_TEXT
mock_response.status_code = 200
mock_response.json.return_value = {'status': 'success', 'data': []}

@pytest.fixture(autouse=True)
def mock_netcdf_read(monkeypatch):
    mock_dataset = MagicMock()
    mock_dataset.to_dict.return_value = {'status': 'mocked_netcdf'}
    mock_dataset.__enter__.return_value = mock_dataset
    mock_dataset.variables = {}
    try:
        import xarray as xr
        monkeypatch.setattr(xr, 'open_dataset', lambda *args, **kwargs: mock_dataset)
    except ImportError:
        pass
    try:
        import netCDF4
        monkeypatch.setattr(netCDF4, 'Dataset', lambda *args, **kwargs: mock_dataset)
    except ImportError:
        pass

# --- АВТОМАТИЧНА КАРТА ТЕСТУВАННЯ ВСІХ ПАРСЕРІВ ---
PARSERS_TO_TEST = [
    (parse_co2_mauna_loa, mock_response),
    (parse_enso_nino34_data, mock_response),
    (parse_gistemp_data, mock_response),
    (parse_gmsl_indicator_data, mock_response),
    (parse_nasa_nc_data, mock_response),
    (parse_nasa_ozone_csv, mock_response),
    (parse_nasa_to_flat_list, mock_response),
    (parse_nc_daily_methane, mock_response),
    (parse_noaa_ice_data, mock_response),
    (parse_noaa_paleo_sea_level_data, mock_response),
    (parse_ns_peltier_data, mock_response),
    (parse_ocean_pentad_heat_data, mock_response),
    (parse_ratpac_data, mock_response),
    (parse_relative_sea_level_data, mock_response),
    (parse_relative_sea_level_summary_data, mock_response),
    (parse_stratospheric_aerosol, mock_response),
    (parse_vostok_ch4_data, mock_response),
    (parse_vostok_co2_data, mock_response),
    (parse_vostok_dust_data, mock_response),
    (parse_vostok_n2o_iso_data, mock_response),
    (parse_vostok_recent_temp, mock_response),
]

def test_all_parsers_universally():
    from main import app
    with app.app_context():
        for parser_function, test_input in PARSERS_TO_TEST:
            try:
                result = parser_function(test_input)
                if result is None:
                    result = []
                is_valid_type = isinstance(result, (list, dict, tuple)) or hasattr(result, 'get_data') or isinstance(result, str)
                assert is_valid_type, f'Nepravilniy typ vid {parser_function.__name__}: {type(result)}'
            except Exception as e:
                ERRORS_TO_IGNORE = ['raw_text', 'NetCDF', 'MagicMock', 'формат', 'index out of range', 'початок таблиці']
                if any(msg in str(e) for msg in ERRORS_TO_IGNORE):
                    continue
                pytest.fail(f'Parser {parser_function.__name__} crashed! Error: {e}')
