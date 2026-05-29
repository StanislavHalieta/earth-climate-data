import os
import logging
from urllib.parse import urlparse
from app.services import HTTPRequest

logger = logging.getLogger(__name__)

def create_noaa_session(base_url=None, endpoint=None, hemisphere=None):
    current_endpoint = None
    try:
        # 1. Сценарій: Передано ПОВНИЙ зовнішній лінк (http://... або https://...)
        if endpoint and (str(endpoint).startswith("http://") or str(endpoint).startswith("https://")):
            parsed_url = urlparse(endpoint)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            current_endpoint = parsed_url.path
            if parsed_url.query:
                current_endpoint += f"?{parsed_url.query}"

        # 2. Сценарій: Передано півкулю (N або S) — це 100% щоденний лід на NSIDC
        elif hemisphere is not None:
            # Приводимо до верхнього регістру для безпеки
            hemi = str(hemisphere).upper()
            if hemi not in ["N", "S"]:
                raise ValueError(f"Невалідний параметр півкулі: '{hemisphere}'. Очікується 'N' або 'S'.")
                
            folder = "north" if hemi == "N" else "south"
            filename = f"{hemi}_seaice_extent_daily_v4.0.csv"
            
            base_url = os.getenv("NOAA_DAILY_ICE_URL")  # https://noaadata.apps.nsidc.org/
            current_endpoint = f"NOAA/G02135/{folder}/daily/data/{filename}"

        # 3. Сценарій: Передано відносний шлях — йдемо на головний сервер NOAA
        elif endpoint is not None:
            base_url = base_url or os.getenv("NOAA_BASE_URL")
            current_endpoint = endpoint
            
        else:
            raise ValueError("Необхідно передати або параметр 'hemisphere', або 'endpoint'.")

        # Захист від порожніх конфігів у .env
        if not base_url or not current_endpoint:
            raise ValueError(f"URL не сформовано. base_url: {base_url}, endpoint: {current_endpoint}")

        # Ініціалізація клієнта та виконання запиту
        session = HTTPRequest(base_url=base_url)
        response = session.get(endpoint=current_endpoint)
        
        logger.info(f"✅ Запит до NOAA: {base_url.strip('/')}/{current_endpoint.lstrip('/')}")
        return response

    except Exception as e:
        logger.error(f"❌ ПОМИЛКА сесії NOAA: {str(e)}", exc_info=True)
        return None