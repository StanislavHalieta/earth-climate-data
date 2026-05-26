import pandas as pd
import io

def parse_noaa_ice_data(csv_content):
    # ПЕРЕВІРКА 1: Чи прийшов рядок?
    if not isinstance(csv_content, str):
        return {
            "status": "error", 
            "message": f"Очікувався рядок (str), але отримано {type(csv_content).__name__}",
            "raw_data_received": str(csv_content)[:100] # показуємо шматочок для дебагу
        }

    # ПЕРЕВІРКА 2: Чи це взагалі схоже на CSV від NOAA?
    if "Year" not in csv_content[:100]:
        return {
            "status": "error",
            "message": "Отримані дані не схожі на формат NOAA CSV. Перевірте авторизацію або URL.",
            "content_preview": csv_content[:200]
        }

    try:
        column_names = ['Year', 'Month', 'Day', 'Extent', 'Missing', 'Source_Data']
        
        # Читаємо дані
        df = pd.read_csv(
            io.StringIO(csv_content), 
            skiprows=2, 
            names=column_names, 
            sep=',', 
            skipinitialspace=True
        )
        
        # Конвертуємо дату
        df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        
        # Чистимо результат
        result = df[['date', 'Extent', 'Missing']].copy()
        result['date'] = result['date'].dt.strftime('%Y-%m-%d')
        
        return {
            "status": "success",
            "data": result.to_dict(orient='records')
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Помилка під час обробки таблиці: {str(e)}"
        }