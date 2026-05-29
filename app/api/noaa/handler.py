import os

from dotenv import load_dotenv

from app.constants import NoaaRoutes

from app.helpers import extract_file_from_zip_parser

from app.api.noaa import (noaa_bp,
                            create_noaa_session,
                            parse_ocean_pentad_heat_data,
                            parse_noaa_ice_data,
                            parse_noaa_paleo_sea_level_data,
                            parse_relative_sea_level_data,
                            parse_relative_sea_level_summary_data,
                            parse_enso_nino34_data,
                            parse_co2_mauna_loa,
                            parse_nc_daily_methane,
                            parse_ratpac_data
                            )

load_dotenv()


@noaa_bp.route("/")
def get_noaa_home():
    
    return "NOAA home"

@noaa_bp.route(NoaaRoutes.NORTH_ICE, methods=["GET"])
def get_north_ice_extent():
    raw_data = create_noaa_session(hemisphere="N")
    if isinstance(raw_data, bytes):
        csv_text = raw_data.decode('utf-8')
    else:
        csv_text = raw_data
        
    parsed_data = parse_noaa_ice_data(csv_text)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.SOUTH_ICE, methods=["GET"])
def get_south_ice_extent():
    raw_data = create_noaa_session(hemisphere="S")
    if isinstance(raw_data, bytes):
        csv_text = raw_data.decode('utf-8')
    else:
        csv_text = raw_data
        
    parsed_data = parse_noaa_ice_data(csv_text)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.PALEO_SEA_LEVEL, methods=["GET"])
def get_paleo_sea_level():
    endpoint = os.getenv("NOAA_PALEO_URL")
    raw_data = create_noaa_session(endpoint=endpoint)
    if isinstance(raw_data, bytes):
        csv_text = raw_data.decode('utf-8')
    else:
        csv_text = raw_data
        
    parsed_data = parse_noaa_paleo_sea_level_data(csv_text)
    
    return parsed_data


@noaa_bp.route(NoaaRoutes.RELATIVE_SEA_LEVEL_SUMMARY, methods=["GET"])
def get_relative_sea_level_summary():
    endpoint = os.getenv("NOAA_PALEO_RELATIVE_SEA_LEVEL_SUMMARY")
    raw_data = create_noaa_session(endpoint=endpoint)
    
    if isinstance(raw_data, bytes):
        csv_text = raw_data.decode('utf-8')
    else:
        csv_text = raw_data
        
    parsed_data = parse_relative_sea_level_summary_data(csv_text)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.RELATIVE_SEA_LEVEL, methods=["GET"])
def get_relative_sea_level():
    endpoint = os.getenv("NOAA_PALEO_RELATIVE_SEA_LEVEL")
    raw_data = create_noaa_session(endpoint=endpoint)
    if isinstance(raw_data, bytes):
        csv_text = raw_data.decode('utf-8')
    else:
        csv_text = raw_data
        
    parsed_data = parse_relative_sea_level_data(csv_text)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.OCEAN_PENTAD_HEAT_0_700, methods=["GET"])
def get_ocean_pentad_heat_data():
    endpoint = os.getenv("NOAA_OCEAN_PENTAD_HEAT")
    raw_data = create_noaa_session(endpoint=endpoint)

    parsed_data = parse_ocean_pentad_heat_data(raw_data)
    
    return parsed_data


@noaa_bp.route(NoaaRoutes.OCEAN_PENTAD_HEAT_0_2000, methods=["GET"])
def get_ocean_pentad_heat_0_2000_data():
    endpoint = os.getenv("NOAA_OCEAN_PENTAD_HEAT_0_2000")
    raw_data = create_noaa_session(endpoint=endpoint)

    parsed_data = parse_ocean_pentad_heat_data(raw_data)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.NOAA_DAILY_METHANE_BRW, methods=["GET"])
def get_daily_methane_brw_data():
    endpoint = os.getenv("NOAA_DAILY_METHANE_BRW")
    base_url = os.getenv("NOAA_GML_BASE_URL")
    
    raw_data = create_noaa_session(base_url=base_url, endpoint=endpoint)
    parsed_data = parse_nc_daily_methane(raw_data)
    
    return parsed_data
    return raw_data

@noaa_bp.route(NoaaRoutes.NOAA_DAILY_METHANE_MLO, methods=["GET"])
def get_daily_methane_mlo_data():
    endpoint = os.getenv("NOAA_DAILY_METHANE_MLO")
    base_url = os.getenv("NOAA_GML_BASE_URL")
    
    raw_data = create_noaa_session(base_url=base_url, endpoint=endpoint)
    parsed_data = parse_nc_daily_methane(raw_data)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.NOAA_RATPAC_A, methods=["GET"])
def get_daily_methane_ratpac_a_data():
    endpoint = os.getenv("NOAA_RATPAC_A")
    
    raw_data = create_noaa_session(endpoint=endpoint)
    unzipped_data = extract_file_from_zip_parser(raw_data)
    parsed_data = parse_ratpac_data(unzipped_data)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.SOLAR_FLUX, methods=["GET"])
def get_solar_flux_data():
    base_url = os.getenv("NOAA_SERVICES_BASE_URL")
    endpoint = os.getenv("NOAA_SOLAR_FLUX")
    
    solar_flux_data = create_noaa_session(base_url=base_url,endpoint=endpoint)
    
    return solar_flux_data

@noaa_bp.route(NoaaRoutes.SUNSPOT, methods=["GET"])
def get_sunpot_data():
    base_url = os.getenv("NOAA_SERVICES_BASE_URL")
    endpoint = os.getenv("NOAA_SUNSPOT")
    
    sunpot_data = create_noaa_session(base_url=base_url,endpoint=endpoint)
    
    return sunpot_data

@noaa_bp.route(NoaaRoutes.KP_INDEX, methods=["GET"])
def get_kp_index_data():
    base_url = os.getenv("NOAA_SERVICES_BASE_URL")
    endpoint = os.getenv("NOAA_KP_INDEX")
    
    kp_index_data = create_noaa_session(base_url=base_url,endpoint=endpoint)
    
    return kp_index_data

@noaa_bp.route(NoaaRoutes.ENSO_NINO34, methods=["GET"])
def get_enso_nino34_data():
    base_url = os.getenv("NOAA_CPC_BASE_URL")
    endpoint = os.getenv("NOAA_ENSO_NINO34")
    
    raw_data = create_noaa_session(base_url=base_url, endpoint=endpoint)
    parsed_data = parse_enso_nino34_data(raw_data)
    
    return parsed_data

@noaa_bp.route(NoaaRoutes.CO2_MAUNA_LOA, methods=["GET"])
def get_co2_mauna_loa_data():
    base_url = os.getenv("NOAA_GML_BASE_URL")
    endpoint = os.getenv("NOAA_CO2_MAUNA_LOA")
    
    raw_data = create_noaa_session(base_url=base_url, endpoint=endpoint)
    parsed_data = parse_co2_mauna_loa(raw_data)
    
    return parsed_data