import io
from netCDF4 import Dataset

def parse_nc_daily_methane(binary_content: bytes) -> list[dict]:
    """
    Парсить бінарний NetCDF (.nc) файл від NOAA з даними про метан 
    і повертає список об'єктів для API.
    """
    if not binary_content:
        return []

    json_data = []

    try:
        # Читаємо бінарні дані прямо з пам'яті за допомогою io.BytesIO
        # Флаг memory=binary_content дозволяє netCDF4 працювати без збереження файлу на диск
        with Dataset("in_memory.nc", memory=binary_content) as nc:
            # 🕵️‍♂️ Дивимося, які змінні є у файлі. 
            # Для щоденних даних NOAA зазвичай використовуються: 'time', 'value', 'year', 'month', 'day'
            
            # Перевіряємо наявність базових полів часу та значень
            if "time" not in nc.variables or "value" not in nc.variables:
                return []

            times = nc.variables["time"][:]
            values = nc.variables["value"][:]
            
            # Якщо у файлі є готові масиви для дат (year, month, day) — беремо їх
            years = nc.variables["year"][:] if "year" in nc.variables else None
            months = nc.variables["month"][:] if "month" in nc.variables else None
            days = nc.variables["day"][:] if "day" in nc.variables else None

            # Ітеруємося по масиву даних
            for i in range(len(values)):
                # Відсікаємо масковані/пропущені значення (NaN або за замовчуванням -999.9)
                val = float(values[i])
                if val < 0:  # У NOAA пропущені дані часто позначаються як -999.99
                    continue

                # Формуємо красиву дату
                date_str = None
                if years is not None and months is not None and days is not None:
                    date_str = f"{int(years[i])}-{int(months[i]):02d}-{int(days[i]):02d}"

                row = {
                    "date": date_str,
                    "methane_ppm": round(val, 2), # Значення концентрації метану
                    "time_epoch": float(times[i])  # Внутрішній час системи
                }
                json_data.append(row)

    except Exception as e:
        # Додай логування помилки за потреби, щоб бачити, якщо файл пошкоджено
        print(f"Помилка парсингу NetCDF: {e}")
        return []

    return json_data