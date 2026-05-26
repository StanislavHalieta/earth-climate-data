def parse_dap_csv(raw_text):
    if not raw_text or not raw_text.strip():
        return []
        
    lines = raw_text.strip().split('\n')
    data_dict = {}
    
    for line in lines:
        if not line:
            continue
        parts = line.split(',')
        var_name = parts[0].strip('/')  # Убираем слеши на начале названия переменной
        values = [float(x) for x in parts[1:] if x.strip()]
        data_dict[var_name] = values
    
    results = []
    times = data_dict.get('time', [])
    
    total_change = data_dict.get('global_average_sea_level_change', [])
    ais = data_dict.get('AIS_mean', [])
    gris = data_dict.get('GrIS_mean', [])
    thermo = data_dict.get('global_average_thermosteric_sea_level_change_lower', [])

    for i in range(len(times)):
        try:
            results.append({
                "date_index": times[i],
                "total_change": total_change[i] if i < len(total_change) else 0.0,
                "ice_sheets": (ais[i] if i < len(ais) else 0.0) + (gris[i] if i < len(gris) else 0.0),
                "thermosteric": thermo[i] if i < len(thermo) else 0.0
            })
        except Exception:
            continue 
            
    return results