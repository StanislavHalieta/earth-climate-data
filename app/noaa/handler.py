import os
from dotenv import load_dotenv
from flask import Blueprint

from app.noaa.noaa_ice_data_parser import parse_noaa_ice_data

from .session import create_noaa_session


load_dotenv()

noaa_bp = Blueprint("noaa", __name__)

@noaa_bp.route("/north_ice_extent")
def north_ice_extent():
    raw_data = create_noaa_session(hemisphere="N")
    parsed_data = parse_noaa_ice_data(raw_data)
    return parsed_data

@noaa_bp.route("/south_ice_extent")
def south_ice_extent():
    raw_data = create_noaa_session(hemisphere="S")
    parsed_data = parse_noaa_ice_data(raw_data)
    return parsed_data