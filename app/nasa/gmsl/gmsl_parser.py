import math
import numpy as np
from datetime import datetime

def format_gmsl_data(data_list):
    if len(data_list) < 2: 
        return {"error": "Critical data insufficiency"}

    # --- КОНСТАНТИ КРАХУ ---
    # 2000 мм (2 метри) — точка неповернення для світової інфраструктури
    CRITICAL_THRESHOLD = 2000.0 
    
    # 1. ПІДГОТОВКА ЧАСОВОЇ ШКАЛИ
    # Використовуємо date_index для точності
    t_first = 1992 + (data_list[0]['date_index'] / 365.25)
    t_last = 1992 + (data_list[-1]['date_index'] / 365.25)
    
    # Рівень у мм (множимо на 10, якщо дані в см)
    h_first = data_list[0]['total_change']
    h_last = data_list[-1]['total_change']
    
    timespan = t_last - t_first
    observed_rise = h_last - h_first

    # 2. РОЗРАХУНОК АГРЕСІЇ ПОТОКУ (Momentum)
    v_total = observed_rise / timespan if timespan > 0 else 0
    
    # Адаптивне вікно (останні 10% даних) для виявлення миттєвого прискорення
    window = max(2, len(data_list) // 10)
    v_recent_dt = t_last - (1992 + (data_list[-window]['date_index'] / 365.25))
    v_recent = (h_last - data_list[-window]['total_change']) / v_recent_dt

    # Коефіцієнт агресії (наскільки швидкість зараз вища за середню)
    aggression_factor = abs(v_recent / v_total) if v_total != 0 else 1.0

    # 3. ДИНАМІЧНИЙ КОЕФІЦІЄНТ К (Кривизна експоненти)
    # Чим вища агресія, тим крутіша крива небезпеки
    k_dynamic = max(2.0, min(10.0, 3.5 * aggression_factor))

    # 4. ЕНЕРГЕТИЧНИЙ БОРГ (The Thermal Debt)
    # p — це відношення реального підйому до критичного порогу (0.0 до 1.0)
    p = max(0.0001, observed_rise / CRITICAL_THRESHOLD)

    # 5. НЕЛІНІЙНА ФУНКЦІЯ HAZARD (Експоненціальний розрахунок)
    # Формула: (e^(k*p) - 1) / (e^k - 1)
    # Це нормалізує значення в діапазоні [0, 1]
    hazard_raw = (math.exp(k_dynamic * p) - 1) / (math.exp(k_dynamic) - 1)

    return {
        "acceleration_index": round(v_recent - v_total, 5),
        "compatibility_protocol": "GENOMIC_DATA_INTEGRATION",
        "date": datetime.now().strftime("%d-%m-%Y"),
        "hazard_index": round(hazard_raw, 12),
        "model": "QUANTUM_MOMENTUM_V17",
        "multi_source_coefficients": {
            "potential_energy_debt": "CRITICAL" if hazard_raw > 0.7 else "HIGH",
            "v_recent_mm_yr": round(v_recent, 4),
            "v_total_mm_yr": round(v_total, 4),
            "k_factor": round(k_dynamic, 2)
        },
        "observed_rise_mm": round(observed_rise, 4)
    }