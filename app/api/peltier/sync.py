# app/api/peltier/sync.py
import os
from app.services import DatabaseService, HTTPRequest
from app.helpers import decompress_gz_file
from app.api.peltier import parse_ns_peltier_data

db = DatabaseService()

def sync_peltier_data():
    print("\n--- Синхронізація домену Peltier ---")
    print("⏳ Обробка Peltier GZ Data...")
    
    base_url_peltier = os.getenv("PELTIER_BASE_URL")
    endpoint_peltier = os.getenv("PELTIER_DATA")
    
    session_peltier = HTTPRequest(base_url=base_url_peltier)
    gz_data = session_peltier.get(endpoint_peltier, verify=False)
    
    unpacked_peltier = decompress_gz_file(gz_data)
    peltier_data = parse_ns_peltier_data(unpacked_peltier)
    
    db.save_metric("peltier_data", peltier_data)
