import netCDF4
import numpy as np

def parse_nasa_nc_data(binary_content):
	"""
	Парсер для бінарних даних NetCDF (.nc)
	binary_content: результат session.get(endpoint)
	"""
	if isinstance(binary_content, str):
		binary_content = binary_content.encode('utf-8', errors='ignore')
 
	try:
		# Відкриваємо бінарний потік як MemoryFile
		with netCDF4.Dataset("in_memory.nc", mode="r", memory=binary_content) as ds:
			# Витягуємо ключові змінні (назви можуть трохи відрізнятися в залежності від версії)
			# Зазвичай у JPL_RECON_GMSL це 'time', 'gmsl' або 'global_average_sea_level_change'
			
			time_data = ds.variables['time'][:]
			gmsl_data = ds.variables['global_average_sea_level_change'][:]
			
			# Додаткові фактори для термодинамічного розрахунку
			# Якщо AIS/GrIS відсутні в цьому конкретному файлі, ставимо 0
			ais = ds.variables.get('AIS_mean', np.zeros_like(time_data))[:]
			gris = ds.variables.get('GrIS_mean', np.zeros_like(time_data))[:]
			thermosteric = ds.variables.get('global_average_thermosteric_sea_level_change', np.zeros_like(time_data))[:]

			results = []
			for i in range(len(time_data)):
				# Перетворюємо маску NetCDF у звичайні числа, ігноруючи NaN
				val_gmsl = float(gmsl_data[i]) if not np.isnan(gmsl_data[i]) else 0.0
				
				results.append({
					"date_index": float(time_data[i]),
					"total_change": val_gmsl,
					"ice_sheets": float(ais[i] + gris[i]),
					"thermosteric": float(thermosteric[i])
				})
			
			return results

	except Exception as e:
		return {"error": f"Failed to parse .nc file: {str(e)}"}