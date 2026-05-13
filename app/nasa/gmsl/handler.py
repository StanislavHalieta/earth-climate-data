import os
from dotenv import load_dotenv
from app.helpers import parse_dap_csv
from app.nasa.gmsl import format_gmsl_data
from app.nasa.session import create_nasa_session # твій клас

load_dotenv()

def get_current_sea_level():
    session = create_nasa_session() 
    url = os.getenv("OPENDAP_URL") + os.getenv("CSL_URL")
    response = session.get(url)
    
    if response.status_code == 200:
        data_json = parse_dap_csv(response.text)  # Конвертуємо CSV у JSON
        formatted_data = format_gmsl_data(data_json)  # Форматуємо дані для фронтенду
        # return formatted_data
        return data_json
    else:
        return f"Помилка: {response.status_code}"