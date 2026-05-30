import re
from flask import jsonify
from app.helpers.date_parsers import decimal_to_date


def parse_gmsl_indicator_data(raw_data: str):
    if isinstance(raw_data, str):
        parts = re.split(r"HDR Header_End-+", raw_data)
        if len(parts) < 2:
            return jsonify({"error": "Не знайдено маркер кінця хедера"}), 500

        raw_data = parts[-1].strip()

        json_list = []
        for line in raw_data.split("\n"):
            columns = line.split()
            if len(columns) >= 3:  # Перевірка на мінімальну кількість колонок
                try:
                    decimal_val = float(columns[0])
                    json_list.append(
                        {
                            "date": decimal_to_date(decimal_val),
                            "decimal_year": decimal_val,
                            "gmsl": float(columns[1]),
                            "smoothed": float(columns[2]),
                        }
                    )
                except (ValueError, IndexError):
                    continue  # Пропускаємо биті рядки
        return jsonify(json_list)
    else:
        return jsonify({"error": "Невірний формат даних"}), 500
