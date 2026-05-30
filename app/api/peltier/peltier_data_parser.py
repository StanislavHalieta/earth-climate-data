from flask import jsonify
import netCDF4


def parse_ns_peltier_data(ns_data):
    with netCDF4.Dataset("peltier_data.nc", memory=ns_data) as nc:
        target_var = (
            "stdev" if "stdev" in nc.variables else list(nc.variables.keys())[-1]
        )

        lats = nc.variables["lat"][:]
        lons = nc.variables["lon"][:]
        data_matrix = nc.variables[target_var][:]

        points = []
        # Матриця NetCDF зазвичай має розмірність [len(lats), len(lons)]
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                # Витягуємо значення. float() потрібен, щоб конвертувати типи NumPy у звичайні Python флоти
                value = float(data_matrix[i, j])

                # Ігноруємо пусті значення (NoData / NaN / Masked values), якщо вони є
                if value == value:  # швидка перевірка на NaN
                    points.append(
                        {
                            "lat": float(lat),
                            "lon": float(lon),
                            "value": round(value, 5),  # округлимо для краси
                        }
                    )

        return jsonify(
            {
                "status": "success",
                "variable_name": target_var,
                "total_points": len(points),
                "points": points,
            }
        )
