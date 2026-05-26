import csv
import io

def parse_gistemp_data(raw_bytes) -> list:
    """
    Парсить виключно файл NASA GISTEMP (GLB.Ts+dSST.csv).
    Приймає дані з response.content (bytes).
    """
    # Декодуємо байтовий рядок у текст
    raw_text = raw_bytes.decode("utf-8")

    result = []
    
    f = io.StringIO(raw_text.strip())
    reader = csv.reader(f)
    
    columns = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        "J-D", "D-N", "DJF", "MAM", "JJA", "SON"
    ]

    for row in reader:
        if not row:
            continue
            
        row_clean = [cell.strip() for cell in row]
        
        # Фільтруємо системні заголовки
        if row_clean[0].startswith("GLOBAL") or row_clean[0] == "Year" or "sources" in row_clean[0]:
            continue
            
        try:
            year = int(row_clean[0])
            year_obj = {"year": year}
            
            for idx, col_name in enumerate(columns):
                val_idx = idx + 1
                
                if val_idx < len(row_clean):
                    val_raw = row_clean[val_idx]
                    
                    if "*" in val_raw or val_raw == "":
                        year_obj[col_name] = None
                    else:
                        year_obj[col_name] = round(float(val_raw) / 100.0, 2)
                else:
                    year_obj[col_name] = None
                    
            result.append(year_obj)
            
        except ValueError:
            continue

    return result