from dotenv import load_dotenv

from app.constants import NasaRoutes
from app.services import DatabaseService
from . import nasa_bp

load_dotenv()

db = DatabaseService()


@nasa_bp.route("/")
def fetch_nasa_home():
    return "NASA home"


@nasa_bp.route(NasaRoutes.GMSL_INDICATOR, methods=["GET", "POST"])
def fetch_gmsl_indicator_raw():
    return db.get_metric("nasa_gmsl_indicator")


@nasa_bp.route(NasaRoutes.GMSL, methods=["GET", "POST"])
def fetch_gmsl():
    return db.get_metric("nasa_gmsl")


@nasa_bp.route(NasaRoutes.OZONE, methods=["GET"])
def fetch_ozone():
    return db.get_metric("nasa_ozone")


@nasa_bp.route(NasaRoutes.GISTEMP)
def fetch_gistemp():
    return db.get_metric("nasa_gistemp")


@nasa_bp.route(NasaRoutes.STRATOSPHERIC_AEROSOL)
def fetch_stratospheric_aerosols():
    return db.get_metric("nasa_stratospheric_aerosol")
