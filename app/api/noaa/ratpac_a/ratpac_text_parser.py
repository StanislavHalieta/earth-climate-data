def parse_ratpac_data(raw_text: str) -> dict:
    """
    Парсить файл RATPAC-A від NOAA, динамічно розбиваючи дані за регіонами 
    (NH, SH, GL тощо) для максимальної читабельності JSON структури.
    """
    if not raw_text or not isinstance(raw_text, str):
        return {}
    
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    result_data = {}
    current_region = "UNKNOWN"
    headers = []

    for line in lines:
        values = line.split()
        if not values:
            continue

        # 1. Перевіряємо, чи це рядок із заголовками висот/тиску
        if "year" in values and "surf" in values:
            headers = values
            continue

        # 2. Якщо перший елемент не число і це не заголовки — значить, це новий регіон (NH, SH, GL...)
        if not values[0].isdigit():
            current_region = values[0]
            # Ініціалізуємо новий масив під цей регіон, якщо його ще немає
            if current_region not in result_data:
                result_data[current_region] = []
            continue

        # 3. Якщо це рядки з даними (перший елемент — число/рік)
        if headers and current_region != "UNKNOWN":
            year = int(values[0])
            row_dict = {"year": year}

            # Мапимо кожну цифру на свій заголовок висоти
            for i, header in enumerate(headers[1:]):
                try:
                    row_dict[header] = float(values[i + 1])
                except (IndexError, ValueError):
                    row_dict[header] = None

            result_data[current_region].append(row_dict)

    return result_data