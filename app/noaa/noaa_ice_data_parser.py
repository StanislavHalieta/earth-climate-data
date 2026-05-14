import pandas as pd
import io

def parse_noaa_ice_data(csv_content):
    # Пропускаємо перші 2 рядки (текстовий опис та рядок з YYYY, MM, DD)
    # Призначаємо зрозумілі імена колонок самостійно
    column_names = ['Year', 'Month', 'Day', 'Extent', 'Missing', 'Source_Data']
    
    df = pd.read_csv(
        io.StringIO(csv_content), 
        skiprows=2, 
        names=column_names, 
        sep=',', 
        skipinitialspace=True
    )
    
    # Конвертуємо в формат дати
    df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    
    # Вибираємо чисті дані
    result = df[['date', 'Extent', 'Missing']].copy()
    
    # Перетворюємо дату в рядок для JSON
    result['date'] = result['date'].dt.strftime('%Y-%m-%d')
    
    return result.to_dict(orient='records')