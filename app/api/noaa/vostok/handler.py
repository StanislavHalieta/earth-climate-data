import os
from dotenv import load_dotenv

from app.api.noaa.session import create_noaa_session
from app.constants import VostokRoutes

from app.api.noaa.vostok import (parse_vostok_ch4_data,
                                 parse_vostok_co2_data,
                                 parse_vostok_dust_data,
                                 parse_vostok_recent_temp,
                                 parse_vostok_n2o_iso_data,
                                 vostok_bp)


load_dotenv()


@vostok_bp.route("/")
def get_vostok_home():
    
    return f"Vostok home"

@vostok_bp.route(VostokRoutes.CO2NAT, methods=["GET"])
def get_vostok_co2_data():
    endpoint = os.getenv("NOAA_PALEO_VOSTOK_CO2NAT")
    
    raw_data = create_noaa_session(endpoint=endpoint)
    parsed_data = parse_vostok_co2_data(raw_data)
    
    return parsed_data

@vostok_bp.route(VostokRoutes.TEMP, methods=["GET"])
def get_vostok_temp_data():
    endpoint = os.getenv("NOAA_PALEO_VOSTOK_TEMP")
    
    raw_data = create_noaa_session(endpoint=endpoint)
    parsed_data = parse_vostok_recent_temp(raw_data)
    
    return parsed_data

@vostok_bp.route(VostokRoutes.CH4NAT, methods=["GET"])
def get_vostok_ch4_data():
    endpoint = os.getenv("NOAA_PALEO_VOSTOK_CH4NAT")
    
    raw_data = create_noaa_session(endpoint=endpoint)
    parsed_data = parse_vostok_ch4_data(raw_data)
    
    return parsed_data

@vostok_bp.route(VostokRoutes.DUSTNAT, methods=["GET"])
def get_vostok_dust_data():
    endpoint = os.getenv("NOAA_PALEO_VOSTOK_DUSTNAT")
    
    raw_data = create_noaa_session(endpoint=endpoint)
    parsed_data = parse_vostok_dust_data(raw_data)
    
    return parsed_data

@vostok_bp.route(VostokRoutes.N2O_ISO, methods=["GET"])
def get_vostok_n2o_iso_data():
    endpoint = os.getenv("NOAA_PALEO_VOSTOK_N2O")
    
    raw_data = create_noaa_session(endpoint=endpoint)
    parsed_data = parse_vostok_n2o_iso_data(raw_data)
    
    return parsed_data