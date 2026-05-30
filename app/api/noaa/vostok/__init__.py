from flask import Blueprint

from app.constants import Blueprints, NoaaRoutes

from app.api.noaa.vostok.co2nat.vostok_co2_nat_parser import parse_vostok_co2_data
from app.api.noaa.vostok.ch4nat.vostok_ch4nat_parser import parse_vostok_ch4_data
from app.api.noaa.vostok.dustnat_noaa.dustnat_noaa_parser import parse_vostok_dust_data
from app.api.noaa.vostok.temp.vostok_temp_parser import parse_vostok_recent_temp
from app.api.noaa.vostok.n2o_iso.n2o_iso_parser import parse_vostok_n2o_iso_data

vostok_bp = Blueprint(Blueprints.VOSTOK, __name__, url_prefix=NoaaRoutes.VOSTOK)

from . import handler

__all__ = [
    "vostok_bp",
    "parse_vostok_co2_data",
    "parse_vostok_ch4_data",
    "parse_vostok_dust_data",
    "parse_vostok_recent_temp",
    "parse_vostok_n2o_iso_data",
]
