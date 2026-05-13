import os
from dotenv import load_dotenv
from .nc_nasa_parser import parse_nasa_nc_data
from app.nasa.session import create_nasa_session

load_dotenv()

def get_current_sea_level():
    session = create_nasa_session()
    endpoint = os.getenv("NASA_SSH_GMSL_DATA_URL")
    response = session.get(endpoint, auth_required=True)
    data = parse_nasa_nc_data(response)
    return data