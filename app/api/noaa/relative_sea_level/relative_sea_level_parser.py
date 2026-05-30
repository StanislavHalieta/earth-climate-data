def parse_relative_sea_level_data(raw_text):
    if not isinstance(raw_text, str):
        return {
            "status": "error",
            "message": f"Очікувався рядок, отримано {type(raw_text)}",
        }

    try:
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
        result_datasets = []

        line_idx = 0
        while line_idx < len(lines):
            current_line = lines[line_idx]
            parts = current_line.split()

            # Перевіряємо, чи це рядок заголовка локації
            # Зазвичай він починається з ID (інтуїтивно ціле число) і має назву в кінці
            if (
                len(parts) >= 5
                and parts[0].isdigit()
                and "." in parts[1]
                and "." in parts[2]
            ):
                station_id = int(parts[0])
                lat = float(parts[1])
                lon = float(parts[2])
                data_rows_count = int(parts[3])  # Скільки рядків даних іде далі

                # Збираємо назву локації (все, що залишилося в рядку після цифр)
                location_name = " ".join(parts[4:])

                station_data = {
                    "station_id": station_id,
                    "location": location_name,
                    "latitude": lat,
                    "longitude": lon,
                    "records": [],
                }

                # Зсуваємо покажчик на наступний рядок, щоб почати збір числових даних
                line_idx += 1

                # Зчитуємо рівно data_rows_count рядків
                for _ in range(data_rows_count):
                    if line_idx >= len(lines):
                        break

                    data_parts = lines[line_idx].split()
                    if len(data_parts) >= 4:
                        age_bp = float(data_parts[0])
                        error_val = float(data_parts[1])
                        sea_level = float(data_parts[2])
                        extra_param = float(data_parts[3])

                        station_data["records"].append(
                            {
                                "calendar_year": int(
                                    2026 - age_bp
                                ),  # Перевод у шкалу нашого часу
                                "age_bp": age_bp,
                                "error": error_val,
                                "sea_level_m": sea_level,
                                "raw_param": extra_param,
                            }
                        )
                    line_idx += 1

                result_datasets.append(station_data)
            else:
                # Якщо рядок не підійшов під шаблон, просто йдемо далі
                line_idx += 1

        return {
            "status": "success",
            "metadata": {
                "format": "NOAA Hierarchical DAT",
                "total_stations_parsed": len(result_datasets),
            },
            "datasets": result_datasets,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Помилка ієрархічного парсингу: {str(e)}",
        }
