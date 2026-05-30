import math


def format_gmsl_indicator_data(data_list):
    if len(data_list) < 2:
        return {"error": "Critical data insufficiency"}

    CRITICAL_THRESHOLD = 2000.0

    t_first, h_first = data_list[0]["decimal_year"], data_list[0]["gmsl"] * 10.0
    t_last, h_last = data_list[-1]["decimal_year"], data_list[-1]["gmsl"] * 10.0

    timespan = t_last - t_first
    observed_rise = h_last - h_first

    v_total = observed_rise / timespan if timespan > 0 else 0
    # Останні 10% масиву (адаптивне вікно для будь-якої довжини даних)
    window = max(2, len(data_list) // 10)
    v_recent = (h_last - (data_list[-window]["gmsl"] * 10.0)) / (
        t_last - data_list[-window]["decimal_year"]
    )

    # 1. ЗАХИСТ ВІД ВІД'ЄМНИХ ВЕКТОРІВ (Absolute Momentum)
    # Ми беремо абсолютне значення для агресії, але враховуємо напрямок у вердикті
    # Це запобігає "вивертанню" експоненти
    aggression_factor = abs(v_recent / v_total) if v_total != 0 else 1.0

    # 2. ДИНАМІЧНИЙ КОЕФІЦІЄНТ К (З обмеженням зверху)
    # k має бути в межах [2.0, 10.0], щоб не ламати математику на великих масштабах
    k_dynamic = max(2.0, min(10.0, 3.5 * aggression_factor))

    # 3. ЕНЕРГЕТИЧНИЙ БОРГ (The Thermal Debt)
    # Навіть якщо вода впала (v_recent < 0), накопичений підйом (observed_rise) нікуди не зник
    p = max(0.0001, observed_rise / CRITICAL_THRESHOLD)

    hazard_raw = (math.exp(k_dynamic * p) - 1) / (math.exp(k_dynamic) - 1)

    return {
        "date": data_list[-1]["date"],
        "observed_rise_mm": round(observed_rise, 4),
        "acceleration_index": round(v_recent / v_total if v_total != 0 else 0, 6),
        "hazard_index": round(max(0.015, hazard_index_final(hazard_raw, v_recent)), 12),
        "multi_source_coefficients": {
            "v_recent_mm_yr": round(v_recent, 4),
            "v_total_mm_yr": round(v_total, 4),
            "potential_energy_debt": (
                "HIGH" if v_recent < 0 and observed_rise > 50 else "STABLE"
            ),
        },
        "model": "QUANTUM_MOMENTUM_V17",
        "compatibility_protocol": "GENOMIC_DATA_INTEGRATION",
    }


def hazard_index_final(raw, v_recent):
    # Якщо швидкість від'ємна ("відкат"), ми тримаємо індекс стабільним (не даємо йому впасти)
    # Це і є врахування "пружини"
    return (
        raw if v_recent >= 0 else raw * 1.2
    )  # +20% до небезпеки за "приховану енергію"
