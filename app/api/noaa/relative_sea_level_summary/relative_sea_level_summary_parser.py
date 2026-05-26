import pandas as pd
import io
import numpy as np

def parse_relative_sea_level_summary_data(raw_text):
    if not isinstance(raw_text, str):
        return {"status": "error", "message": f"Очікувався рядок, отримано {type(raw_text)}"}

    try:
        # 1. Відсікаємо всі рядки коментарів з решіткою #
        lines = [line for line in raw_text.split('\n') if line.strip() and not line.startswith('#')]
        
        if not lines:
            return {"status": "error", "message": "Файл не містить копії корисних даних"}

        # 2. Визначаємо назви колонок. Оскільки реальний заголовок файлу занадто довгий 
        # і містить пробіли, ми закладемо чисті короткі назви з опису метаданих (Variables)
        target_columns = [
            'latitude', 'longitude', 'references', 
            'age_older_limit', 'age_younger_limit', 'age_mean', 
            'classification', 'rsl', 'limit_elev', 'elev_err_up', 'elev_err_down'
        ]

        # 3. Пропускаємо перші 2 рядки (текстовий заголовок та рядок з цифрами 3, 4, 8...)
        # і зчитуємо решту даних через регулярний вираз для табуляцій/пробілів
        data_lines = lines[2:]
        
        df = pd.read_csv(
            io.StringIO('\n'.join(data_lines)), 
            sep='\t', 
            names=target_columns,
            header=None,
            skipinitialspace=True
        )

        # 4. Обробка пропущених значень (наприклад, порожні клітинки стануть NaN)
        df = df.replace({np.nan: None})

        # 5. Конвертація у чисті Python-типи для безпечної серіалізації в JSON (Flask сумісність)
        result_records = []
        for _, row in df.iterrows():
            result_records.append({
                "latitude": float(row['latitude']),
                "longitude": float(row['longitude']),
                "references": str(row['references']).strip(),
                "calendar_year": int(2026 - int(row['age_mean'])), # Розрахунок відносного року для індексу
                "age_mean_cal_bp": int(row['age_mean']),
                "age_range_2sigma": [int(row['age_younger_limit']), int(row['age_older_limit'])],
                "classification": str(row['classification']).strip(),
                "rsl_meters": float(row['rsl']) if row['rsl'] is not None else None,
                "limit_elev_meters": float(row['limit_elev']) if row['limit_elev'] is not None else None,
                "errors": {
                    "up": float(row['elev_err_up']) if row['elev_err_up'] is not None else None,
                    "down": float(row['elev_err_down']) if row['elev_err_down'] is not None else None
                }
            })

        return {
            "status": "success",
            "metadata": {
                "dataset": "Central US Gulf Coast Holocene Relative Sea-Level",
                "investigators": "Hijma, M.P.; Tornqvist, T.E. (2015)",
                "records_count": len(result_records)
            },
            "data": result_records
        }

    except Exception as e:
        return {"status": "error", "message": f"Критична помилка парсингу: {str(e)}"}