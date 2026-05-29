def parse_stratospheric_aerosol(raw_data: str) -> dict:

    if isinstance(raw_data, bytes):
        raw_text = raw_data.decode('utf-8')
    else:
        raw_text = raw_data
        
    months_keys = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    seasonal_keys = ['J-D', 'D-N', 'DJF', 'MAM', 'JJA', 'SON']
    
    parsed_results = []
    
    # Розбиваємо текст на рядки
    lines = raw_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        # Пропускаємо пусті рядки або заголовок
        if not line or line.startswith("Land-Ocean:") or line.startswith("Year"):
            continue
            
        # Розбиваємо рядок за комами або пробілами (залежно від того, як прийшов сирий текст)
        # Оскільки в копіпасті дані розділені комами, ділимо по комі
        parts = [p.strip() for p in line.split(',')]
        
        # Перевірка, чи це валідний рядок з роком (має бути мінімум 19 колонок)
        if len(parts) < 19:
            continue
            
        try:
            year = int(parts[0])
            
            # Внутрішня функція для конвертації значень (зірочки міняємо на None)
            def to_float_or_none(val: str):
                return None if '***' in val or not val else float(val)
            
            # Збираємо місяці (індекси 1-12)
            monthly_data = {}
            for idx, month in enumerate(months_keys):
                monthly_data[month] = to_float_or_none(parts[idx + 1])
                
            # Збираємо сезонні та річні агрегати (індекси 13-18)
            aggregates = {}
            for idx, season in enumerate(seasonal_keys):
                aggregates[season] = to_float_or_none(parts[idx + 13])
                
            # Формуємо об'єкт для конкретного року
            year_entry = {
                "year": year,
                "monthly": monthly_data,
                "aggregates": aggregates
            }
            
            parsed_results.append(year_entry)
            
        except ValueError as e:
            # Якщо перший елемент не рік — пропускаємо цей рядок
            print(f"⚠️ Пропущено некоректний рядок: {line} (Помилка: {e})")
            continue

    return {
        "status": "success",
        "source": "NASA GISS Surface Temperature Analysis",
        "total_years": len(parsed_results),
        "data": parsed_results
    }