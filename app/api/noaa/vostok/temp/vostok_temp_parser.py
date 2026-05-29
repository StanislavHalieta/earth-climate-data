import pandas as pd
import io
import numpy as np

def parse_vostok_recent_temp(raw_data):
    
    if isinstance(raw_data, bytes):
        raw_text = raw_data.decode('utf-8')
    else:
        raw_text = raw_data
        
    if not isinstance(raw_text, str):
        return {"status": "error", "message": f"Очікувався рядок, отримано {type(raw_text)}"}

    try:
        # 1. Відфільтровуємо коментарі (рядки з решіткою #)
        lines = [line for line in raw_text.split('\n') if line.strip() and not line.startswith('#')]
        
        if not lines:
            return {"status": "error", "message": "Файл не містить корисних даних або порожній"}

        # 2. Зчитуємо дані (розділювач табуляція/пробіли)
        clean_data = '\n'.join(lines)
        df = pd.read_csv(io.StringIO(clean_data), sep='\s+')

        # Перевірка наявності потрібних колонок
        if 'age_CE' not in df.columns or 'tempanom' not in df.columns:
            return {"status": "error", "message": f"Не знайдено колонки 'age_CE' або 'tempanom'. Наявні: {list(df.columns)}"}

        # 3. Очищення від NaN значень для безпеки JSON
        df = df.replace({np.nan: None})

        # 4. Конвертація у базові типи Python (запобігає TypeError: Object of type int64...)
        result_records = []
        for _, row in df.iterrows():
            year_ce = row['age_CE']
            temp_anom = row['tempanom']
            
            result_records.append({
                "calendar_year": int(year_ce),
                "temperature_anomaly_celsius": float(temp_anom) if temp_anom is not None else None
            })

        return {
            "status": "success",
            "metadata": {
                "dataset": "Vostok 350 Year Ice Core Temperature Reconstruction",
                "authors": "Ekaykin, A.A. et al. (2014)",
                "source": "NOAA Paleoclimatology Program",
                "time_range": f"{result_records[-1]['calendar_year']} - {result_records[0]['calendar_year']}",
                "records_count": len(result_records)
            },
            "data": result_records
        }

    except Exception as e:
        return {"status": "error", "message": f"Помилка парсингу температурних даних: {str(e)}"}