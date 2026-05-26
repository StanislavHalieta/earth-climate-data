import os
from dotenv import load_dotenv

from app.constants import NasaRoutes

from app.api.nasa import nasa_bp
from app.api.nasa.gmsl import parse_nasa_nc_data
from app.api.nasa.ozone import get_latest_nasa_ozone_url, parse_nasa_to_flat_list
from app.api.nasa.gmsl_indicator.calculate_index import calculate_gmsl_indicator_index
from app.api.nasa.gistemp.gistemp_parser import parse_gistemp_data

from app.api.nasa.session import create_nasa_session


load_dotenv()


session = create_nasa_session()

@nasa_bp.route("/")
def fetch_nasa_home():
    
    return f"NASA home"

@nasa_bp.route(NasaRoutes.GMSL_INDICATOR, methods=["GET", "POST"])
def fetch_gmsl_indicator_raw():
    endpoint = os.getenv("NASA_SSH_GMSL_INDICATOR_URL", "")
    raw_data = session.get(endpoint=endpoint, auth_required=True)
    death_index = calculate_gmsl_indicator_index(raw_data)
    return death_index

@nasa_bp.route(NasaRoutes.GMSL, methods=["GET", "POST"])
def fetch_gmsl():
    endpoint = os.getenv("NASA_SSH_GMSL_DATA_URL")
    raw_data = session.get(endpoint=endpoint, auth_required=True)
    json_data = parse_nasa_nc_data(raw_data)
    return json_data

@nasa_bp.route(NasaRoutes.OZONE, methods=["GET"])
def fetch_ozone():
    base_url = os.getenv("NASA_ARCHIVE_GESDISC_URL")
    endpoint = get_latest_nasa_ozone_url()
    session = create_nasa_session(base_url=base_url)
    
    raw_data = session.get(endpoint=endpoint, auth_required=True)
    parsed_data = parse_nasa_to_flat_list(raw_data)
    return parsed_data

@nasa_bp.route(NasaRoutes.GISTEMP)
def fetch_gistemp():
    base_url = os.getenv("NASA_GISS_BASE_URL")
    endpoint = os.getenv("NASA_GISSTEMP")
    
    session = create_nasa_session(base_url=base_url)
    
    raw_data = session.get(endpoint=endpoint, auth_required=True)
    parsed_gistemp_data = parse_gistemp_data(raw_data)
    
    return parsed_gistemp_data