import xarray as xr
import json

def convert_nc_to_json(file_path):
    # Відкриваємо бінарний файл NASA
    ds = xr.open_dataset(file_path)
    
    # Витягаємо час та рівень моря (GMSL)
    # Назви змінних у JPL_RECON можуть бути 'time' та 'gmsl'
    df = ds.to_dataframe().reset_index()
    
    data_list = []
    for _, row in df.iterrows():
        data_list.append({
            "decimal_year": float(row['time']),
            "gmsl": float(row['gmsl']) / 10.0, # Конвертуємо мм у см, якщо NASA дає в мм
            "date": str(row['time']) # Спрощено
        })
    
    return data_list