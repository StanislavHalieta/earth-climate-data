from flask import jsonify
from app.helpers.http_request import HTTPRequest # твій клас


def get_current_sea_level():
    # Використовуємо наш універсальний клас
    client = HTTPRequest(base_url="https://climate.nasa.gov")
    
    # Припустимо, ми забираємо дані (ендпоінт для прикладу)
    data = client.get("/api/v1/gmsl")
    
    return jsonify({
        "module": "NASA GML",
        "raw_data": data,
        "hazard_index": "TENSOR_ACCELERATION_V16" 
    })