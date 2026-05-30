import os
import psycopg
from flask import Response, current_app
from dotenv import load_dotenv

from app.constants import NoaaRoutes
from . import noaa_bp

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")


def get_data_from_db(key_name: str):
    """Універсальна функція для читання JSON із бази даних."""
    if not DB_URL:
        current_app.logger.error("DATABASE_URL is not set!")
        return {"error": "Database configuration error"}, 500

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT payload FROM climate_data WHERE key_name = %s;", (key_name,)
                )
                row = cur.fetchone()
                if row and row[0]:
                    payload = row[0]
                    if isinstance(payload, str):
                        return Response(payload, mimetype="application/json")
                    import json

                    return Response(json.dumps(payload), mimetype="application/json")

                return {"error": f"Data for '{key_name}' not synced yet"}, 404
    except Exception as e:
        current_app.logger.error(f"Database error: {e}")
        return {"error": "Internal database error"}, 500


@noaa_bp.route("/")
def get_noaa_home():
    return "NOAA home"


@noaa_bp.route(NoaaRoutes.NORTH_ICE, methods=["GET"])
def get_north_ice_extent():
    return get_data_from_db("noaa_north_ice")


@noaa_bp.route(NoaaRoutes.SOUTH_ICE, methods=["GET"])
def get_south_ice_extent():
    return get_data_from_db("noaa_south_ice")


@noaa_bp.route(NoaaRoutes.PALEO_SEA_LEVEL, methods=["GET"])
def get_paleo_sea_level():
    return get_data_from_db("noaa_paleo_sea_level")


@noaa_bp.route(NoaaRoutes.RELATIVE_SEA_LEVEL_SUMMARY, methods=["GET"])
def get_relative_sea_level_summary():
    return get_data_from_db("noaa_relative_sea_level_summary")


@noaa_bp.route(NoaaRoutes.RELATIVE_SEA_LEVEL, methods=["GET"])
def get_relative_sea_level():
    return get_data_from_db("noaa_relative_sea_level")


@noaa_bp.route(NoaaRoutes.OCEAN_PENTAD_HEAT_0_700, methods=["GET"])
def get_ocean_pentad_heat_data():
    return get_data_from_db("noaa_ocean_pentad_heat_0_700")


@noaa_bp.route(NoaaRoutes.OCEAN_PENTAD_HEAT_0_2000, methods=["GET"])
def get_ocean_pentad_heat_0_2000_data():
    return get_data_from_db("noaa_ocean_pentad_heat_0_2000")


@noaa_bp.route(NoaaRoutes.NOAA_DAILY_METHANE_BRW, methods=["GET"])
def get_daily_methane_brw_data():
    return get_data_from_db("noaa_methane_brw")


@noaa_bp.route(NoaaRoutes.NOAA_DAILY_METHANE_MLO, methods=["GET"])
def get_daily_methane_mlo_data():
    return get_data_from_db("noaa_methane_mlo")


@noaa_bp.route(NoaaRoutes.NOAA_RATPAC_A, methods=["GET"])
def get_daily_methane_ratpac_a_data():
    return get_data_from_db("noaa_ratpac_a")


@noaa_bp.route(NoaaRoutes.SOLAR_FLUX, methods=["GET"])
def get_solar_flux_data():
    return get_data_from_db("noaa_solar_flux")


@noaa_bp.route(NoaaRoutes.SUNSPOT, methods=["GET"])
def get_sunpot_data():
    return get_data_from_db("noaa_sunspot")


@noaa_bp.route(NoaaRoutes.KP_INDEX, methods=["GET"])
def get_kp_index_data():
    return get_data_from_db("noaa_kp_index")


@noaa_bp.route(NoaaRoutes.ENSO_NINO34, methods=["GET"])
def get_enso_nino34_data():
    return get_data_from_db("noaa_enso_nino34")


@noaa_bp.route(NoaaRoutes.CO2_MAUNA_LOA, methods=["GET"])
def get_co2_mauna_loa_data():
    return get_data_from_db("noaa_co2_mauna_loa")
