import os

from app.api.peltier import peltier_bp, parse_ns_peltier_data
from app.helpers import decompress_gz_file, HTTPRequest

@peltier_bp.route("/")
def get_peltier_home():
    base_url = os.getenv("PELTIER_BASE_URL")
    endpoint = os.getenv("PELTIER_DATA")
    
    session = HTTPRequest(base_url=base_url)
    gz_data = session.get(endpoint, verify=False)
    
    unpacked_data = decompress_gz_file(gz_data)
    
    parsed_data = parse_ns_peltier_data(unpacked_data)
    
    return parsed_data