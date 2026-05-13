import os
from dotenv import load_dotenv
from flask import Blueprint

from app.nasa.gmsl import get_current_sea_level
from app.nasa.gmsl_indicator import get_gmsl_indicator_data
from app.nasa.session import create_nasa_session


load_dotenv()

nasa_bp = Blueprint("nasa", __name__)

@nasa_bp.route("/gmsl_indicator", methods=["GET", "POST"])
def fetch_gmsl_indicator_raw():
    session = create_nasa_session()
    endpoint=os.getenv("NASA_SSH_GMSL_INDICATOR_URL", "")
    response = session.get(endpoint, auth_required=True)

    return get_gmsl_indicator_data(response)

@nasa_bp.route("/gmsl", methods=["GET", "POST"])
def gmsl_endpoint():
    return get_current_sea_level()