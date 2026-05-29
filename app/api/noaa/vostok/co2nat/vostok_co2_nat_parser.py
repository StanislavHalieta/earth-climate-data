import pandas as pd
import io
import numpy as np

def parse_vostok_co2_data(raw_data):
    
    if isinstance(raw_data, bytes):
        raw_text = raw_data.decode('utf-8')
    else:
        raw_text = raw_data
        
    if not isinstance(raw_text, str):
        return {"status": "error", "message": f"Очікувався рядок, отримано {type(raw_text)}"}

    try:
        # 1. Фільтруємо коментарі (все, що починається з #)
        lines = [line for line in raw_text.split('\n') if line.strip() and not line.startswith('#')]
        
        if not lines:
            return {"status": "error", "message": "Файл порожній або містить лише коментарі"}

        # 2. Зчитуємо дані через pandas (розділювач табуляція)
        clean_data = '\n'.join(lines)
        df = pd.read_csv(io.StringIO(clean_data), sep='\t', skipinitialspace=True)

        # Перевіряємо наявність потрібних колонок
        if 'gas_ageBP' not in df.columns or 'CO2' not in df.columns:
            return {"status": "error", "message": f"Не знайдено колонки 'gas_ageBP' або 'CO2'. Наявні: {list(df.columns)}"}

        # 3. Обробка пропущених значень
        df = df.replace({np.nan: None})

        # 4. Конвертація у чисті типи Python для уникнення TypeError при серіалізації в JSON
        result_records = []
        for _, row in df.iterrows():
            age_bp = float(row['gas_ageBP'])
            co2_val = row['CO2']
            
            # Робимо перетворення типів
            result_records.append({
                "calendar_year": int(2026 - int(age_bp)), # Розраховуємо абсолютний рік від 2026-го
                "years_ago_bp": int(age_bp),
                "co2_ppm": float(co2_val) if co2_val is not None else None
            })

        return {
            "status": "success",
            "metadata": {
                "dataset": "Vostok Ice Core - Atmospheric Carbon Dioxide Data",
                "authors": "Petit, J.-R. et al. (1999)",
                "source": "NOAA Paleoclimatology Program",
                "records_count": len(result_records)
            },
            "data": result_records
        }

    except Exception as e:
        return {"status": "error", "message": f"Помилка парсингу Vostok data: {str(e)}"}