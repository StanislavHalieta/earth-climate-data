import io
import xarray as xr
import numpy as np
import pandas as pd


def parse_ocean_pentad_heat_data(binary_content, depth_layer="0-2000"):
    """
    Парсер бінарних NetCDF (.nc) файлів тепломісткості океану від NOAA.
    Працює автономно без сторонніх плагінів для кодування часу.
    """
    try:
        if not binary_content or not isinstance(binary_content, bytes):
            return {
                "status": "error",
                "message": "Очікувався бінарний контент (bytes) NetCDF файлу",
            }

        # 🛠️ КЛЮЧОВИЙ МОМЕНТ: Відкриваємо БЕЗ автоматичного декодування часу,
        # щоб xarray не падав через кастомні календарі NOAA
        with xr.open_dataset(
            io.BytesIO(binary_content), engine="h5netcdf", decode_times=False
        ) as ds:

            # Автоматично шукаємо наукову змінну, що відповідає за аномалію тепла
            hc_var_name = [
                v for v in ds.data_vars if "hc" in v or "heat" in v or "anom" in v
            ]
            if not hc_var_name:
                hc_var_name = [list(ds.data_vars)[0]]

            var_to_extract = hc_var_name[0]

            # Агрегуємо просторові координати: рахуємо середнє по всій планеті
            spatial_dims = [
                dim
                for dim in ["lat", "lon", "latitude", "longitude"]
                if dim in ds[var_to_extract].dims
            ]
            global_trend = ds[var_to_extract].mean(dim=spatial_dims, skipna=True)

            result_records = []

            if "time" in global_trend.coords:
                time_values = global_trend.time.values
                anomaly_values = global_trend.values

                # Читаємо рядок юнітів часу з метаданих файлу (наприклад, "months since 1955-01-01 00:00:00")
                time_units = ds.time.attrs.get("units", "months since 1955-01-01")

                # Витягуємо базову дату (все, що після слова 'since')
                base_date_str = time_units.split("since")[-1].strip()
                try:
                    base_date = pd.Timestamp(base_date_str)
                except Exception:
                    base_date = pd.Timestamp(
                        "1955-01-01"
                    )  # залізобетонний фолбек для NOAA OHC

                # Проходимо по масиву
                for i in range(len(time_values)):
                    # Витягуємо чисте число через .item() або індекс, щоб уникнути помилки скалярів
                    try:
                        raw_val = (
                            anomaly_values[i].item()
                            if hasattr(anomaly_values[i], "item")
                            else float(anomaly_values[i])
                        )
                        raw_time = (
                            time_values[i].item()
                            if hasattr(time_values[i], "item")
                            else int(time_values[i])
                        )
                    except Exception:
                        # Фолбек, якщо це чисті numpy типи без методу .item()
                        raw_val = float(anomaly_values[i])
                        raw_time = int(time_values[i])

                    if np.isnan(raw_val):
                        continue

                    # Рахуємо дату (додаємо сирі місяці до базової дати)
                    months_offset = int(raw_time)
                    calculated_date = base_date + pd.DateOffset(months=months_offset)
                    time_str = calculated_date.strftime("%Y-%m-%d")

                    result_records.append(
                        {
                            "date_period": time_str,
                            "heat_anomaly_value_10_22_joules": round(raw_val, 4),
                        }
                    )

            return {
                "status": "success",
                "metadata": {
                    "dataset": f"Ocean Heat Content Anomaly ({depth_layer}m)",
                    "source": "NOAA National Centers for Environmental Information (NCEI)",
                    "extracted_variable": var_to_extract,
                    "total_records": len(result_records),
                },
                "data": result_records,
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Помилка обробки NetCDF файлу {depth_layer}: {str(e)}",
        }
