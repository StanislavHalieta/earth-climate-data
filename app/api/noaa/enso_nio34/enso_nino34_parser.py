def parse_enso_nino34_data(raw_data: str) -> dict:
    # Перевіряємо щоб був текст, якщо ні то декодуємо бінарні дані
    if isinstance(raw_data, bytes):
        raw_text = raw_data.decode("utf-8")
    else:
        raw_text = raw_data

    parsed_results = []

    # Розбиваємо текст на рядки
    lines = raw_text.strip().split("\n")

    for line in lines:
        line = line.strip()

        # Пропускаємо пусті рядки та рядок заголовка (наприклад, той що починається з YR або MON)
        if not line or line.startswith("YR") or line.startswith("MON"):
            continue

        # .split() без аргументів ідеально ділить по будь-якій кількості пробілів
        parts = line.split()

        # У валідному рядку має бути рівно 10 значень (Рік, Місяць + 4 пари SST/ANOM)
        if len(parts) != 10:
            continue

        try:
            year = int(parts[0])
            month = int(parts[1])

            # Збираємо дані по конкретних зонах
            entry = {
                "year": year,
                "month": month,
                "regions": {
                    "nino1_2": {"sst": float(parts[2]), "anom": float(parts[3])},
                    "nino3": {"sst": float(parts[4]), "anom": float(parts[5])},
                    "nino4": {"sst": float(parts[6]), "anom": float(parts[7])},
                    "nino3_4": {"sst": float(parts[8]), "anom": float(parts[9])},
                },
            }
            parsed_results.append(entry)

        except ValueError as e:
            # На випадок бітих даних
            print(f"⚠️ Пропущено некоректний рядок: {line} | Помилка: {e}")
            continue

    return {
        "status": "success",
        "source": "NOAA Climate Prediction Center (Niño Regions)",
        "total_records": len(parsed_results),
        "data": parsed_results,
    }
