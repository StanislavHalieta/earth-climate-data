import os
from flask.cli import load_dotenv
import requests

load_dotenv()

def create_nasa_session():
    # 1. Збираємо дані з .env
    user = os.getenv("NASA_USER")
    password = os.getenv("NASA_PASS")
    raw_base_url = os.getenv("ARCHIVE_PODAAC_URL")

    # 2. Перевірка наявності облікових даних та URL
    if not all([user, password, raw_base_url]):
        missing = [name for name, val in [
            ("NASA_USER", user), 
            ("NASA_PASS", password), 
            ("ARCHIVE_PODAAC_URL", raw_base_url)
        ] if not val]
        # Викидаємо виключення, бо без конфігу додаток не має сенсу запускати
        raise ValueError(f"Критична помилка конфігурації .env. Відсутні: {', '.join(missing)}")

    # 3. Валідація формату URL
    if not raw_base_url.startswith(("http://", "https://")):
        raise ValueError(f"Некоректний ARCHIVE_PODAAC_URL: має починатися з http/https. Отримано: {raw_base_url}")

    # 4. Створення сесії
    session = requests.Session()
    session.auth = (user, password)
    
    # Очищуємо URL від зайвих пробілів та слешів в кінці
    session.base_url = raw_base_url.strip().rstrip('/')
    
    # 5. Додаємо стандартні хедери (корисно для NASA API)
    session.headers.update({
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "NASA-Data-Client-v1.0"
    })

    return session