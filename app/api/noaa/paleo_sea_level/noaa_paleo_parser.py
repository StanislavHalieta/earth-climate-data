import pandas as pd
import io


def parse_noaa_paleo_sea_level_data(raw_txt_data):
    # ПЕРЕВІРКА: якщо прийшов не текст, а помилка від сервера у форматі dict
    if isinstance(raw_txt_data, dict):
        return {
            "error": "Server returned a dictionary, not data",
            "content": raw_txt_data,
        }

    if not isinstance(raw_txt_data, str):
        return {"error": f"Expected string, got {type(raw_txt_data)}"}

    try:
        # Відсікаємо заголовок (все, що з #)
        lines = [
            l for l in raw_txt_data.split("\n") if l.strip() and not l.startswith("#")
        ]

        if not lines:
            return {"error": "No data found after skipping comments"}

        # Читаємо дані (використовуємо sep='\s+' для табів і пробілів)
        df = pd.read_csv(io.StringIO("\n".join(lines)), sep="\s+")

        # Мапінг колонок (виправляє KeyError)
        mapping = {"age_calkaBP": "age_ka", "SeaLev_shortPC1": "sea_level"}
        df.rename(columns=mapping, inplace=True)

        # Фільтрація для "планетарної загрози" (останні 50к років)
        if "age_ka" in df.columns:
            df_filtered = df[df["age_ka"] <= 50].copy()

            # перетворюємо типи pandas/numpy у звичайні python типи
            result_data = []
            for _, row in df_filtered.iterrows():
                result_data.append(
                    {
                        "year": int(2026 - (row["age_ka"] * 1000)),
                        "age_ka": float(row["age_ka"]),
                        "sea_level": float(row["sea_level"]),
                    }
                )
            return {"type": "paleo", "data": result_data}

        return {"error": "Required columns not found"}

    except Exception as e:
        return {"error": f"Parser error: {str(e)}"}
