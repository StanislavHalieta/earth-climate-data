import os
from dotenv import load_dotenv

from app.helpers import HTTPRequest


load_dotenv()

def create_noaa_session(hemisphere="N"):
    folder = "north" if hemisphere == "N" else "south"
    filename = f"{hemisphere}_seaice_extent_daily_v4.0.csv"
    endpoint = f"NOAA/G02135/{folder}/daily/data/{filename}"
    session = HTTPRequest(base_url=os.getenv("NOAA_BASE_URL"))
    endpoint = os.getenv("NOAA_ICE_URL")
    response = session.get(endpoint=endpoint)
    return response
