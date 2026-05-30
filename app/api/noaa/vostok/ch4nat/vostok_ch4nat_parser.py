import pandas as pd
import io
import numpy as np


def parse_vostok_ch4_data(raw_data):
    if isinstance(raw_data, bytes):
        raw_text = raw_data.decode("utf-8")
    else:
        raw_text = raw_data
    if not isinstance(raw_text, str):
        return {
            "status": "error",
            "message": f"Очікувався рядок, отримано {type(raw_text)}",
        }

    try:
        # 1. Очищаємо від коментарів (рядків з #)
        lines = [
            line
            for line in raw_text.split("\n")
            if line.strip() and not line.startswith("#")
        ]

        if not lines:
            return {
                "status": "error",
                "message": "Файл не містить корисних даних (тільки коментарі або порожній)",
            }

        # 2. Зчитуємо дані через pandas (розділювач табуляція)
        clean_data = "\n".join(lines)
        df = pd.read_csv(io.StringIO(clean_data), sep="\t", skipinitialspace=True)

        # Валідація колонок
        if "gas_ageBP" not in df.columns or "CH4" not in df.columns:
            return {
                "status": "error",
                "message": f"Не знайдено колонки 'gas_ageBP' або 'CH4'. Наявні: {list(df.columns)}",
            }

        # 3. Безпечна заміна NaN для JSON серіалізації
        df = df.replace({np.nan: None})

        # 4. Конвертація в чисті Python типи (захист від int64/float64 помилок у Flask)
        result_records = []
        for _, row in df.iterrows():
            age_bp = row["gas_ageBP"]
            ch4_val = row["CH4"]

            result_records.append(
                {
                    "calendar_year": int(
                        2026 - int(age_bp)
                    ),  # Абсолютний календарний рік
                    "years_ago_bp": int(age_bp),
                    "ch4_ppb": float(ch4_val) if ch4_val is not None else None,
                }
            )

        return {
            "status": "success",
            "metadata": {
                "dataset": "Vostok Ice Core - Atmospheric Methane (CH4) Data",
                "authors": "Petit, J.-R. et al. (1999)",
                "source": "NOAA Paleoclimatology Program",
                "records_count": len(result_records),
            },
            "data": result_records,
        }

    except Exception as e:
        return {"status": "error", "message": f"Помилка парсингу Vostok CH4: {str(e)}"}
