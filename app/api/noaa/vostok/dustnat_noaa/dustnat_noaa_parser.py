import pandas as pd
import io
import numpy as np

def parse_vostok_dust_data(raw_text):
    if not isinstance(raw_text, str):
        return {"status": "error", "message": f"Очікувався рядок, отримано {type(raw_text)}"}

    try:
        # 1. Фільтруємо коментарі (рядки з решіткою #)
        lines = [line for line in raw_text.split('\n') if line.strip() and not line.startswith('#')]
        
        if not lines:
            return {"status": "error", "message": "Файл порожній або містить лише метадані"}

        # 2. Зчитуємо таблицю (розділювач табуляція)
        clean_data = '\n'.join(lines)
        df = pd.read_csv(io.StringIO(clean_data), sep='\t', skipinitialspace=True)

        # Валідація колонок
        if 'ice_ageBP' not in df.columns or 'dust_ppm' not in df.columns:
            return {"status": "error", "message": f"Не знайдено колонки 'ice_ageBP' або 'dust_ppm'. Наявні: {list(df.columns)}"}

        # 3. Заміна NaN значень на None для сумісності з JSON
        df = df.replace({np.nan: None})

        # 4. Конвертація у базові типи Python
        result_records = []
        for _, row in df.iterrows():
            ice_age = row['ice_ageBP']
            dust_val = row['dust_ppm']
            
            result_records.append({
                "calendar_year": int(2026 - int(ice_age)), # Перерахунок в абсолютну шкалу часу від 2026 року
                "ice_age_bp": int(ice_age),
                "dust_concentration_ppm": float(dust_val) if dust_val is not None else None
            })

        return {
            "status": "success",
            "metadata": {
                "dataset": "Vostok Ice Core - Dust Concentration Data",
                "authors": "Petit, J.-R. et al. (1999)",
                "source": "NOAA Paleoclimatology Program (GT4 Chronology)",
                "records_count": len(result_records)
            },
            "data": result_records
        }

    except Exception as e:
        return {"status": "error", "message": f"Помилка парсингу Vostok Dust: {str(e)}"}