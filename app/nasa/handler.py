import os
from dotenv import load_dotenv
from flask import Blueprint

from app.nasa.pdaac.handler import get_clean_nasa_data
from app.nasa.session import create_nasa_session


load_dotenv()

nasa_bp = Blueprint("NASA", __name__)

@nasa_bp.route("/GMSL")
def fetch_gmsl_indicator_raw():
    session = create_nasa_session()
    endpoint=os.getenv("NASA_SSH_GMSL_INDICATOR_URL", "").lstrip('/')
    response = session.get(f"{session.base_url}/{endpoint}")

    if response.status_code != 200:
        return {"error": f"NASA Indicator Error: {response.status_code}"}
    
    return get_clean_nasa_data(response.text)

@nasa_bp.route("/GMSL_INDICATOR")
def gmsl_indicator_endpoint():        
    return get_clean_nasa_data()