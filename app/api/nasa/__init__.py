from flask import Blueprint

from app.constants import (Blueprints, ApiRoutes)

from app.api.nasa.session import create_nasa_session
from app.api.nasa.gistemp import parse_gistemp_data
from app.api.nasa.gmsl import parse_nasa_nc_data
from app.api.nasa.gmsl_indicator.gmsl_indicator_parser import  hazard_index_final
from app.api.nasa.gmsl_indicator.gmsl_indicator_data_parser import parse_gmsl_indicator_data
from app.api.nasa.ozone.ozone_data_parser import parse_nasa_ozone_csv, parse_nasa_to_flat_list
from app.api.nasa.ozone.fresh_link_generator import get_latest_nasa_ozone_url
from app.api.nasa.stratospheric_aerosol.stratospheric_aerosol_parser import parse_stratospheric_aerosol
from app.api.nasa.sync import sync_nasa_data

nasa_bp = Blueprint(Blueprints.NASA, __name__, url_prefix=ApiRoutes.NASA)

from . import handler

__all__ = ["nasa_bp",
           "sync_nasa_data",
           "create_nasa_session",
           "parse_gistemp_data",
           "parse_nasa_nc_data",
           "hazard_index_final",
           "parse_gmsl_indicator_data",
           "parse_nasa_ozone_csv",
           "parse_nasa_to_flat_list",
           "get_latest_nasa_ozone_url",
           "parse_stratospheric_aerosol"
           ]