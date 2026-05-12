import os

from app.helpers.http_request import HTTPRequest
from app.helpers import parse_dap_csv
from app.nasa.session import create_nasa_session # твій клас



def get_current_sea_level():
    session = create_nasa_session() 
    # session має використовувати AUTH (Basic або Bearer)
    
    url = os.getenv("OPENDAP_URL") + "/collections/C2491724765-POCLOUD/granules/global_timeseries_measures.dap.csv"
    
    response = session.get(url)
    
    if response.status_code == 200:
        # return response.text # Тут буде твій CSV
        data_json = parse_dap_csv(response.text)  # Конвертуємо CSV у JSON
        return data_json
    else:
        return f"Помилка: {response.status_code}"