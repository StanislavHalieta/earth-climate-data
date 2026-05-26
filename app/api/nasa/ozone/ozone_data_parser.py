import io

def parse_nasa_ozone_csv(binary_content: bytes) -> dict:
    """
    Парсить оригінальний текстовий дамп HE5 файлу від NASA.
    Збирає суцільні масиви даних та нарізає їх на матрицю 180х360.
    """
    if not binary_content:
        return {"lat": [], "lon": [], "solar_zenith_angle": [], "ozone": []}

    # Декодуємо байти в текст
    text_data = binary_content.decode("utf-8", errors="ignore")
    lines = text_data.splitlines()

    # Словник для збереження чистих "пласких" списків значень по секціях
    sections_data = {
        "lon": [],
        "lat": [],
        "SolarZenithAngle": [],
        "ColumnAmountO3": []
    }

    current_section = None
    FILL_VALUE = -1.26765e+30

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Визначаємо, в якій ми секції. Перевіряємо початок рядка
        if line_stripped.startswith("/lon"):
            current_section = "lon"
            raw_text = line_stripped[4:].lstrip(",") # прибираємо префікс "/lon,"
        elif line_stripped.startswith("/lat"):
            current_section = "lat"
            raw_text = line_stripped[4:].lstrip(",")
        elif line_stripped.startswith("/SolarZenithAngle"):
            current_section = "SolarZenithAngle"
            raw_text = line_stripped[17:].lstrip(",")
        elif line_stripped.startswith("/ColumnAmountO3"):
            current_section = "ColumnAmountO3"
            raw_text = line_stripped[15:].lstrip(",")
        elif line_stripped.startswith("/ViewingZenithAngle") or line_stripped.startswith("/RadiativeCloudFraction") or line_stripped.startswith("/UVAerosolIndex") or line_stripped.startswith("/StructMetadata_0"):
            # Нам ці секції не потрібні, або це кінець файлу
            current_section = None
            continue
        else:
            # Якщо рядок не починається з префіксу — це продовження попередньої секції
            raw_text = line_stripped

        # Якщо ми всередині потрібної секції — парсимо числа через кому
        if current_section:
            parts = raw_text.split(",")
            for part in parts:
                part_clean = part.strip()
                if not part_clean:
                    continue
                try:
                    val_float = float(part_clean)
                    # Якщо це значення-заглушка — залишаємо як є (нічого не викидаємо)
                    sections_data[current_section].append(val_float)
                except ValueError:
                    # Пропускаємо випадковий текст, якщо він проскочить
                    continue

    # --- Нарізка пласких списків у матриці 180 строк на 360 стовпчиків ---
    # Перевіряємо, чи збігаються розміри
    rows, cols = 180, 360
    
    sza_matrix = []
    ozone_matrix = []

    sza_flat = sections_data["SolarZenithAngle"]
    ozone_flat = sections_data["ColumnAmountO3"]

    # Крокуємо по 360 елементів (один рядок довготи) для кожної із 180 широт
    for i in range(rows):
        start_idx = i * cols
        end_idx = start_idx + cols
        
        # Нарізаємо SZA
        row_sza = sza_flat[start_idx:end_idx]
        sza_matrix.append(row_sza)
        
        # Нарізаємо Ozone
        row_ozone = ozone_flat[start_idx:end_idx]
        ozone_matrix.append(row_ozone)

    return {
        "lat": sections_data["lat"],
        "lon": sections_data["lon"],
        "solar_zenith_angle": sza_matrix,
        "ozone": ozone_matrix
    }
    
def parse_nasa_to_flat_list(binary_content: bytes) -> list:
    if isinstance(binary_content, (dict, list)):
        return (
            binary_content  # або витягуємо потрібний ключ, наприклад: raw_data.get('data', raw_data)
        )

    # 2. Перевірка на байти
    if isinstance(binary_content, bytes):
        text_data = binary_content.decode("utf-8", errors="ignore")
    elif isinstance(binary_content, str):
        text_data = binary_content
    else:
        # Якщо прийшло щось зовсім дивне (наприклад, None або число)
        raise TypeError(
            f"Неочікуваний тип даних для парсингу: {type(binary_content)}"
        )

    # Тепер splitlines() ніколи не впаде
    lines = text_data.splitlines()

    sections_data = {
        "lon": [], "lat": [], "SolarZenithAngle": [], "ColumnAmountO3": []
    }
    current_section = None

    # 1. Збираємо всі числа з файлу по своїх секціях
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        if line_stripped.startswith("/lon"):
            current_section = "lon"
            raw_text = line_stripped[4:].lstrip(",")
        elif line_stripped.startswith("/lat"):
            current_section = "lat"
            raw_text = line_stripped[4:].lstrip(",")
        elif line_stripped.startswith("/SolarZenithAngle"):
            current_section = "SolarZenithAngle"
            raw_text = line_stripped[17:].lstrip(",")
        elif line_stripped.startswith("/ColumnAmountO3"):
            current_section = "ColumnAmountO3"
            raw_text = line_stripped[15:].lstrip(",")
        elif line_stripped.startswith("/ViewingZenithAngle") or line_stripped.startswith("/StructMetadata_0"):
            current_section = None
            continue
        else:
            raw_text = line_stripped

        if current_section:
            for part in raw_text.split(","):
                part_clean = part.strip()
                if part_clean:
                    try:
                        sections_data[current_section].append(float(part_clean))
                    except ValueError:
                        continue

    # 2. Мапуємо координати та виміри (ПРАВИЛЬНО)
    result_points = []  # Ініціалізуємо ОДИН РАЗ тут, а не всередині циклу!
    
    latitudes = sections_data["lat"]   # 180 значень
    longitudes = sections_data["lon"]  # 360 значень
    sza_flat = sections_data["SolarZenithAngle"]
    ozone_flat = sections_data["ColumnAmountO3"]

    total_lats = len(latitudes)
    total_lons = len(longitudes)

    # Йдемо по черзі: для кожної широти перебираємо всі довготи
    for y in range(total_lats):
        for x in range(total_lons):
            # Обчислюємо точний індекс елемента в пласкому масиві
            flat_index = y * total_lons + x
            
            # Безпечно беремо значення
            sza_val = sza_flat[flat_index] if flat_index < len(sza_flat) else -1.26765e+30
            ozone_val = ozone_flat[flat_index] if flat_index < len(ozone_flat) else -1.26765e+30

            # Формуємо точку і додаємо її в загальний список
            point = {
                "lat": latitudes[y],
                "lon": longitudes[x],
                "ozone": ozone_val,
                "solar_zenith_angle": sza_val
            }
            result_points.append(point)

    return result_points