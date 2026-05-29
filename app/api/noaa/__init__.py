from flask import Blueprint

from app.api.noaa.vostok import vostok_bp
from app.constants import (Blueprints, ApiRoutes)

from app.api.noaa.session import create_noaa_session
from app.api.noaa.ocean_pentad_heat.ocean_pentad_heat_data import parse_ocean_pentad_heat_data
from app.api.noaa.relative_sea_level.relative_sea_level_parser import parse_relative_sea_level_data
from app.api.noaa.noaa_ice_extent.noaa_ice_data_parser import parse_noaa_ice_data
from app.api.noaa.paleo_sea_level.noaa_paleo_parser import parse_noaa_paleo_sea_level_data
from app.api.noaa.relative_sea_level_summary.relative_sea_level_summary_parser import parse_relative_sea_level_summary_data
from app.api.noaa.co2_mauna_loa.co2_mauna_loa_parser import parse_co2_mauna_loa
from app.api.noaa.enso_nio34.enso_nino34_parser import parse_enso_nino34_data
from app.api.noaa.methane.methane_parser import parse_nc_daily_methane
from app.api.noaa.ratpac_a.ratpac_text_parser import parse_ratpac_data

noaa_bp = Blueprint(Blueprints.NOAA, __name__, url_prefix=ApiRoutes.NOAA)

noaa_bp.register_blueprint(vostok_bp)

from . import handler

__all__ = [
    "noaa_bp",
    "create_noaa_session"
    "parse_ocean_pentad_heat_data",
    "parse_relative_sea_level_data",
    "parse_noaa_ice_data",
    "parse_noaa_paleo_sea_level_data",
    "parse_relative_sea_level_summary_data",
    "parse_enso_nino34_data",
    "parse_co2_mauna_loa",
    "parse_nc_daily_methane",
    "parse_ratpac_data"
]