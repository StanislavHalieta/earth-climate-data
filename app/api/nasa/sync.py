# app/api/nasa/sync.py
import os
from app.services import DatabaseService

from app.api.nasa import (create_nasa_session,
                          parse_nasa_nc_data,
                          parse_stratospheric_aerosol,
                          get_latest_nasa_ozone_url,
                          parse_nasa_to_flat_list,
                          parse_gmsl_indicator_data,
                          parse_gistemp_data)

db = DatabaseService()

def sync_nasa_data():
    print("\n--- Синхронізація домену NASA ---")
    session_nasa = create_nasa_session()
    
    # 1. GMSL Indicator
    endpoint_indicator = os.getenv("NASA_SSH_GMSL_INDICATOR_URL", "")
    raw_indicator = session_nasa.get(endpoint=endpoint_indicator, auth_required=True)
    db.save_metric("nasa_gmsl_indicator", parse_gmsl_indicator_data(raw_indicator))
    
    # 2. GMSL NetCDF
    endpoint_gmsl = os.getenv("NASA_SSH_GMSL_DATA_URL", "")
    raw_gmsl = session_nasa.get(endpoint=endpoint_gmsl, auth_required=True)
    db.save_metric("nasa_gmsl", parse_nasa_nc_data(raw_gmsl))
    
    # 3. Ozone
    base_url_ozone = os.getenv("NASA_ARCHIVE_GESDISC_URL")
    endpoint_ozone = get_latest_nasa_ozone_url()
    session_ozone = create_nasa_session(base_url=base_url_ozone)
    raw_ozone = session_ozone.get(endpoint=endpoint_ozone, auth_required=True)
    db.save_metric("nasa_ozone", parse_nasa_to_flat_list(raw_ozone))
    
    # 4 & 5. Gistemp & Stratospheric Aerosol
    base_url_giss = os.getenv("NASA_GISS_BASE_URL")
    endpoint_gistemp = os.getenv("NASA_GISSTEMP")
    session_giss = create_nasa_session(base_url=base_url_giss)
    raw_gistemp = session_giss.get(endpoint=endpoint_gistemp, auth_required=True)
    db.save_metric("nasa_gistemp", parse_gistemp_data(raw_gistemp))
    db.save_metric("nasa_stratospheric_aerosol", parse_stratospheric_aerosol(raw_gistemp))
