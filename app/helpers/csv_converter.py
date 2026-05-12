def parse_dap_csv(raw_text):
    lines = raw_text.strip().split('\n')
    data_dict = {}

    for line in lines:
        if not line: continue
        # Розділяємо назву змінної та значення
        parts = line.split(',')
        var_name = parts[0].strip('/') # Прибираємо слеші на початку
        values = [float(x) for x in parts[1:] if x.strip()]
        data_dict[var_name] = values

    # Тепер збираємо це в список об'єктів для API
    results = []
    # Використовуємо 'time' як індекс
    for i in range(len(data_dict.get('time', []))):
        results.append({
            "date_index": data_dict['time'][i],
            "total_change": data_dict['global_average_sea_level_change'][i],
            "ice_sheets": data_dict['AIS_mean'][i] + data_dict['GrIS_mean'][i],
            "thermosteric": data_dict['global_average_thermosteric_sea_level_change_lower'][i] # або mean
        })
    
    return results