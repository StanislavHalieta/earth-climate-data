# app/api/noaa/sync.py
import os
from app.services import DatabaseService
from app.helpers import extract_file_from_zip_parser


# app/api/noaa/sync.py
import os
from app.services import DatabaseService
from app.helpers import  extract_file_from_zip_parser

# ПРЯМІ ІМПОРТИ (замість одного загального), щоб уникнути циклічного імпорту:
from app.api.noaa.session import create_noaa_session
from app.api.noaa.ocean_pentad_heat.ocean_pentad_heat_data import parse_ocean_pentad_heat_data
from app.api.noaa.relative_sea_level.relative_sea_level_parser import parse_relative_sea_level_data
from app.api.noaa.noaa_ice_extent.noaa_ice_data_parser import parse_noaa_ice_data
from app.api.noaa.paleo_sea_level.noaa_paleo_parser import parse_noaa_paleo_sea_level_data
from app.api.noaa.relative_sea_level_summary.relative_sea_level_summary_parser import parse_relative_sea_level_summary_data
from app.api.noaa.co2_mauna_loa.co2_mauna_loa_parser import parse_co2_mauna_loa
from app.api.noaa.enso_nio34.enso_nino34_parser import parse_enso_nino34_data
from app.api.noaa.methane.methane_parser import parse_nc_daily_methane
from app.api.noaa.ratpac_a.ratpac_text_parser import parse_ratpac_data
from app.api.noaa.vostok.ch4nat.vostok_ch4nat_parser import parse_vostok_ch4_data
from app.api.noaa.vostok.co2nat.vostok_co2_nat_parser import parse_vostok_co2_data
from app.api.noaa.vostok.dustnat_noaa.dustnat_noaa_parser import parse_vostok_dust_data
from app.api.noaa.vostok.n2o_iso.n2o_iso_parser import parse_vostok_n2o_iso_data
from app.api.noaa.vostok.temp.vostok_temp_parser import parse_vostok_recent_temp

db = DatabaseService()

def sync_noaa_data():
    print("\n--- Синхронізація домену NOAA ---")
    
    # ... весь наявний код синхронізації метрик NOAA 1-15 залишається без змін ...
    
    # ========================================================
    # 🚀 ДОДАЄМО ПІД-БЛОК: СТАНЦІЯ ВОСТОК (Історичні дані)
    # ========================================================
    print("\n--- 🧊 Синхронізація під-домену Vostok (NOAA) ---")
    
    # 1. Vostok CO2
    print("⏳ Обробка Vostok CO2nat...")
    raw_vostok_co2 = create_noaa_session(endpoint=os.getenv("NOAA_PALEO_VOSTOK_CO2NAT"))
    vostok_co2_data = parse_vostok_co2_data(raw_vostok_co2)
    db.save_metric("vostok_co2nat", vostok_co2_data)
    
    # 2. Vostok Temperature
    print("⏳ Обробка Vostok Temperature...")
    raw_vostok_temp = create_noaa_session(endpoint=os.getenv("NOAA_PALEO_VOSTOK_TEMP"))
    vostok_temp_data = parse_vostok_recent_temp(raw_vostok_temp)
    db.save_metric("vostok_temp", vostok_temp_data)
    
    # 3. Vostok Methane (CH4)
    print("⏳ Обробка Vostok CH4nat...")
    raw_vostok_ch4 = create_noaa_session(endpoint=os.getenv("NOAA_PALEO_VOSTOK_CH4NAT"))
    vostok_ch4_data = parse_vostok_ch4_data(raw_vostok_ch4)
    db.save_metric("vostok_ch4nat", vostok_ch4_data)
    
    # 4. Vostok Dust
    print("⏳ Обробка Vostok Dustnat...")
    raw_vostok_dust = create_noaa_session(endpoint=os.getenv("NOAA_PALEO_VOSTOK_DUSTNAT"))
    vostok_dust_data = parse_vostok_dust_data(raw_vostok_dust)
    db.save_metric("vostok_dustnat", vostok_dust_data)
    
    # 5. Vostok N2O Isolation
    print("⏳ Обробка Vostok N2O Isolation...")
    raw_vostok_n2o = create_noaa_session(endpoint=os.getenv("NOAA_PALEO_VOSTOK_N2O"))
    vostok_n2o_data = parse_vostok_n2o_iso_data(raw_vostok_n2o)
    db.save_metric("vostok_n2o_iso", vostok_n2o_data)



def decode_to_text(raw_data):
    """Безпечне перетворення байтів у текст CSV."""
    if isinstance(raw_data, bytes):
        return raw_data.decode('utf-8')
    return raw_data

def sync_noaa_data():
    print("\n--- Синхронізація домену NOAA ---")
    
    # 1. North Ice Extent
    raw_north_ice = create_noaa_session(hemisphere="N")
    north_ice_text = decode_to_text(raw_north_ice)
    north_ice_data = parse_noaa_ice_data(north_ice_text)
    db.save_metric("noaa_north_ice", north_ice_data)
    
    # 2. South Ice Extent
    raw_south_ice = create_noaa_session(hemisphere="S")
    south_ice_text = decode_to_text(raw_south_ice)
    south_ice_data = parse_noaa_ice_data(south_ice_text)
    db.save_metric("noaa_south_ice", south_ice_data)
    
    # 3. Paleo Sea Level
    endpoint_paleo = os.getenv("NOAA_PALEO_URL")
    raw_paleo = create_noaa_session(endpoint=endpoint_paleo)
    paleo_text = decode_to_text(raw_paleo)
    paleo_data = parse_noaa_paleo_sea_level_data(paleo_text)
    db.save_metric("noaa_paleo_sea_level", paleo_data)
    
    # 4. Relative Sea Level Summary
    print("⏳ Обробка Relative Sea Level Summary...")
    endpoint_summary = os.getenv("NOAA_PALEO_RELATIVE_SEA_LEVEL_SUMMARY")
    raw_summary = create_noaa_session(endpoint=endpoint_summary)
    summary_text = decode_to_text(raw_summary)
    summary_data = parse_relative_sea_level_summary_data(summary_text)
    db.save_metric("noaa_relative_sea_level_summary", summary_data)
    
    # 5. Relative Sea Level
    print("⏳ Обробка Relative Sea Level...")
    endpoint_sea_level = os.getenv("NOAA_PALEO_RELATIVE_SEA_LEVEL")
    raw_sea_level = create_noaa_session(endpoint=endpoint_sea_level)
    sea_level_text = decode_to_text(raw_sea_level)
    sea_level_data = parse_relative_sea_level_data(sea_level_text)
    db.save_metric("noaa_relative_sea_level", sea_level_data)
    
    # 6. Ocean Pentad Heat 0-700
    print("⏳ Обробка Ocean Pentad Heat 0-700...")
    endpoint_heat_700 = os.getenv("NOAA_OCEAN_PENTAD_HEAT")
    raw_heat_700 = create_noaa_session(endpoint=endpoint_heat_700)
    heat_700_data = parse_ocean_pentad_heat_data(raw_heat_700)
    db.save_metric("noaa_ocean_pentad_heat_0_700", heat_700_data)
    
    # 7. Ocean Pentad Heat 0-2000
    print("⏳ Обробка Ocean Pentad Heat 0-2000...")
    endpoint_heat_2000 = os.getenv("NOAA_OCEAN_PENTAD_HEAT_0_2000")
    raw_heat_2000 = create_noaa_session(endpoint=endpoint_heat_2000)
    heat_2000_data = parse_ocean_pentad_heat_data(raw_heat_2000)
    db.save_metric("noaa_ocean_pentad_heat_0_2000", heat_2000_data)
    
    # 8. Methane BRW
    print("⏳ Обробка Methane BRW...")
    base_url_gml = os.getenv("NOAA_GML_BASE_URL")
    endpoint_methane_brw = os.getenv("NOAA_DAILY_METHANE_BRW")
    raw_methane_brw = create_noaa_session(base_url=base_url_gml, endpoint=endpoint_methane_brw)
    methane_brw_data = parse_nc_daily_methane(raw_methane_brw)
    db.save_metric("noaa_methane_brw", methane_brw_data)
    
    # 9. Methane MLO
    print("⏳ Обробка Methane MLO...")
    endpoint_methane_mlo = os.getenv("NOAA_DAILY_METHANE_MLO")
    raw_methane_mlo = create_noaa_session(base_url=base_url_gml, endpoint=endpoint_methane_mlo)
    methane_mlo_data = parse_nc_daily_methane(raw_methane_mlo)
    db.save_metric("noaa_methane_mlo", methane_mlo_data)
    
    # 10. Ratpac A (ZIP)
    print("⏳ Обробка Ratpac A...")
    endpoint_ratpac = os.getenv("NOAA_RATPAC_A")
    raw_zip = create_noaa_session(endpoint=endpoint_ratpac)
    unzipped_file = extract_file_from_zip_parser(raw_zip)
    ratpac_data = parse_ratpac_data(unzipped_file)
    db.save_metric("noaa_ratpac_a", ratpac_data)
    
    # 11, 12, 13. Space Weather Services
    print("⏳ Обробка Solar/Space Weather...")
    base_url_services = os.getenv("NOAA_SERVICES_BASE_URL")
    
    # Solar Flux
    endpoint_solar = os.getenv("NOAA_SOLAR_FLUX")
    solar_flux_data = create_noaa_session(base_url=base_url_services, endpoint=endpoint_solar)
    db.save_metric("noaa_solar_flux", solar_flux_data)
    
    # Sunspot
    endpoint_sunspot = os.getenv("NOAA_SUNSPOT")
    sunspot_data = create_noaa_session(base_url=base_url_services, endpoint=endpoint_sunspot)
    db.save_metric("noaa_sunspot", sunspot_data)
    
    # KP Index
    endpoint_kp = os.getenv("NOAA_KP_INDEX")
    kp_index_data = create_noaa_session(base_url=base_url_services, endpoint=endpoint_kp)
    db.save_metric("noaa_kp_index", kp_index_data)
    
    # 14. ENSO Nino34
    print("⏳ Обробка ENSO Nino34...")
    base_url_cpc = os.getenv("NOAA_CPC_BASE_URL")
    endpoint_nino = os.getenv("NOAA_ENSO_NINO34")
    raw_nino = create_noaa_session(base_url=base_url_cpc, endpoint=endpoint_nino)
    nino_data = parse_enso_nino34_data(raw_nino)
    db.save_metric("noaa_enso_nino34", nino_data)
    
    # 15. CO2 Mauna Loa
    print("⏳ Обробка CO2 Mauna Loa...")
    endpoint_co2 = os.getenv("NOAA_CO2_MAUNA_LOA")
    raw_co2 = create_noaa_session(base_url=base_url_gml, endpoint=endpoint_co2)
    co2_data = parse_co2_mauna_loa(raw_co2)
    db.save_metric("noaa_co2_mauna_loa", co2_data)
