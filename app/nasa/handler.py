import os
from dotenv import load_dotenv
from flask import Blueprint

from app.nasa.gmsl.handler import get_current_sea_level
from app.nasa.gmsl_indicator.handler import gmsl_indicator_data
from app.nasa.session import create_nasa_session


load_dotenv()

nasa_bp = Blueprint("nasa", __name__)

@nasa_bp.route("/gmsl_indicator", methods=["GET", "POST"])
def fetch_gmsl_indicator_raw():
    session = create_nasa_session()
    endpoint=os.getenv("NASA_SSH_GMSL_INDICATOR_URL", "").lstrip('/')
    response = session.get(f"{session.base_url}/{endpoint}")

    if response.status_code != 200:
        return {"error": f"NASA Indicator Error: {response.status_code}"}
    
    return gmsl_indicator_data(response.text)

@nasa_bp.route("/GMSL")
def gmsl_endpoint():        
    return get_current_sea_level()