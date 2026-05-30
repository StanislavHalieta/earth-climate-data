import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from app.api.nasa import create_nasa_session


def get_latest_nasa_ozone_url() -> str:
    """
    Автоматично знаходить та генерує посилання на найсвіжіший файл .he5.
    Повертає рядок з повним URL або піднімає виняток у разі повної невдачі.
    """
    current_year = datetime.now().year
    base_url = os.getenv("NASA_ARCHIVE_GESDISC_URL")
    client = create_nasa_session(base_url=base_url)

    # 1. Спроба завантажити каталог для поточного року
    endpoint = (
        f"opendap/HDF-EOS5/Aura_OMI_Level3/OMTO3d.003/{current_year}/contents.html"
    )
    html_data = client.get(endpoint)

    # Перевіряємо, чи не повернув клієнт словник із помилкою (наприклад, 404)
    if isinstance(html_data, dict) and "error" in html_data:
        # Якщо новий рік щойно почався, даних ще немає — відкочуємось на рік назад
        current_year -= 1
        endpoint = (
            f"opendap/HDF-EOS5/Aura_OMI_Level3/OMTO3d.003/{current_year}/contents.html"
        )
        html_data = client.get(endpoint)

        # Якщо і за минулий рік сталася помилка, прокидаємо її далі
        if isinstance(html_data, dict) and "error" in html_data:
            raise RuntimeError(f"NASA catalog global error: {html_data.get('message')}")

    # 2. Парсинг отриманої HTML-сторінки
    soup = BeautifulSoup(html_data, "html.parser")
    pattern = re.compile(
        r"OMI-Aura_L3-OMTO3d_\d{4}m\d{4}_v\d{3}-\d{4}m\d{4}t\d{6}\.he5"
    )

    he5_files = []
    for link in soup.find_all("a", href=True):
        filename = link["href"].split("/")[-1]
        if pattern.match(filename):
            he5_files.append(filename)

    if not he5_files:
        raise FileNotFoundError(
            f"No .he5 files found in NASA catalog for year {current_year}"
        )

    # 3. Сортування за алфавітом/хронологією та вибір останнього елемента
    he5_files.sort()
    latest_filename = he5_files[-1]
    clean_filename = latest_filename.removesuffix(".xml")
    # 4. Формування фінального прямого посилання
    final_endpoint = f"/opendap/HDF-EOS5/Aura_OMI_Level3/OMTO3d.003/{current_year}/{clean_filename}.dap.csv"
    return final_endpoint
