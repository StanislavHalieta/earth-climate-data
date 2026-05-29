# NASA Climate Data Collector (GMSL)

Проєкт для автоматизації збору та обробки наукових даних NASA щодо глобального середнього рівня моря (**Global Mean Sea Level - GMSL**), а також кліматичних показників NOAA. Додаток реалізує повний цикл: від авторизації в захищених архівах NASA до парсингу бінарних NetCDF файлів.

## 🌟 Особливості

* **NASA Earthdata Integration**: Логіка авторизації через `requests.Session` з підтримкою редиректів між доменами.
* **NetCDF4 Parsing**: Автоматичне витягування часових рядів та показників зміни рівня моря з бінарних наукових форматів.
* **Robust Architecture**: Модульна структура з чітким розділенням на обробники (handlers) та допоміжні інструменти (helpers).
* **Security First**: Використання змінних оточення для захисту облікових даних NASA.

## 🛠 Керування залежностями (Poetry)

У цьому проєкту використовується **Poetry** для ізоляції середовища та керування бібліотеками.

### 📥 Встановлення (Перше розгортання)

Встановіть Poetry та pre-commit у вашу систему, розгорніть проєкт ініціалізуйте хуки:

  ```bash
  # Встановлення Poetry (для систем на базі pip)
  pip install poetry

  # Встановлення всіх залежностей проєкту
  poetry install

  # Ініціалізація pre-commit хуків для автоматизації
  poetry run pre-commit install
  ```

## 🚀 Запуск коду та розробка

Усі команди виконуються всередині ізольованого оточення Poetry:

* **Запуск програми:** 
  ```bash
  poetry run python main.py
  ```

* **Запуск автоматичних тестів (pytest):**
  ```bash
  PYTHONPATH=. poetry run pytest
  ```

* **Оновлення внутрішньої документації:**
  ```bash
  poetry run python update_docs.py
  ```

### 🔄 Автоматизація через Pre-commit
У проєкті налаштовано **pre-commit хуки**. Під час кожного збереження змін (`git commit`) автоматично запускаються скрипти:
* **Генерація структури:** Автоматично оновлюється дерево каталогів у розділі `🏗 Структура проєкту`.
* **Оновлення ендпоінтів:** Автоматично збираються нові маршрути в таблицю `📑 Кінцеві точки`.

Якщо ви хочете запустити генерацію дерева та ендпоінтів вручну (без створення коміту), виконайте:
  ```bash
  poetry run pre-commit run --all-files
  ```

### ➕ Робота з бібліотеками

* **Додати нову бібліотеку:**
  ```bash
  poetry add <назва_бібліотеки>
  ```
* **Додати бібліотеку для розробки/тестів:**
  ```bash
  poetry add <назва_бібліотеки> --group dev
  ```
* **Видалити бібліотеку:**
  ```bash
  poetry remove <назва_бібліотеки>
  ```
* **Оновити бібліотеки до свіжих версій:**
  ```bash
  poetry update
  ```

## 🧪 Тестування
Для перевірки працездатності сервера використовується фреймворк `pytest`. Наразі реалізовано базові тести для перевірки доступності кінцевих точок (endpoints). У планах — розширення тестового покриття для парсерів бінарних NetCDF4 файлів та логіки авторизації в NASA Earthdata.


## ⚙️ Налаштування оточення (`.env`)

Створіть файл `.env` у корені проєкту та заповніть його вашими даними:


<!-- START_ENV_EXAMPLE -->

```env
FLASK_ENV=True

#START_ACCESS
NASA_USER=
NASA_PASS=
NASA_TOKEN=
#END_ACCESS

NASA_ARCHIVE_GESDISC_URL=https://acdisc.gesdisc.eosdis.nasa.gov
NASA_ARCHIVE_PODAAC_URL=https://archive.podaac.earthdata.nasa.gov
NASA_GISS_BASE_URL=https://data.giss.nasa.gov

NASA_SSH_GMSL_INDICATOR_URL=/podaac-ops-cumulus-protected/NASA_SSH_GMSL_INDICATOR/NASA_SSH_GMSL_INDICATOR.txt
NASA_SSH_GMSL_DATA_URL=/podaac-ops-cumulus-protected/JPL_RECON_GMSL/global_timeseries_measures.nc
NASA_GISSTEMP=/gistemp/tabledata_v4/GLB.Ts+dSST.csv
NASA_STRATOSPHERIC_AEROSOL=modelforce/strataer/original_GISS_data/tau.line_2012.12.txt


OPENDAP_URL=https://opendap.earthdata.nasa.gov
CSL_URL=/collections/C2491724765-POCLOUD/granules/global_timeseries_measures.dap.csv

# NOAA_BASE_URLS
NOAA_BASE_URL=https://www.ncei.noaa.gov
NOAA_DAILY_ICE_URL=https://noaadata.apps.nsidc.org
NOAA_GML_BASE_URL=https://gml.noaa.gov
NOAA_SERVICES_BASE_URL=https://services.swpc.noaa.gov
NOAA_CPC_BASE_URL=https://www.cpc.ncep.noaa.gov

# URLs generated automatically 
# NOAA_ICE_URL=/NOAA/G02135/north/daily/data/N_seaice_extent_daily_v4.0.csv
# NOAA_ICE_URL=/NOAA/G02135/south/daily/data/S_seaice_extent_daily_v4.0.csv

# Paleo Data URLs
NOAA_PALEO_URL=/pub/data/paleo/contributions_by_author/spratt2016/spratt2016-noaa.txt
NOAA_PALEO_RELATIVE_SEA_LEVEL=/pub/data/paleo/paleocean/relative_sea_level/sealevel.dat
NOAA_PALEO_RELATIVE_SEA_LEVEL_SUMMARY=/pub/data/paleo/paleocean/relative_sea_level/hijma2014rsl-summary.txt
NOAA_PALEO_VOSTOK_CO2NAT=/pub/data/paleo/icecore/antarctica/vostok/co2nat-noaa.txt
NOAA_PALEO_VOSTOK_TEMP=/pub/data/paleo/icecore/antarctica/vostok/vostok2014temp-noaa.txt
NOAA_PALEO_VOSTOK_CH4NAT=/pub/data/paleo/icecore/antarctica/vostok/ch4nat-noaa.txt
NOAA_PALEO_VOSTOK_DUSTNAT=/pub/data/paleo/icecore/antarctica/vostok/dustnat-noaa.txt
NOAA_OCEAN_PENTAD_HEAT=/thredds-ocean/fileServer/woa/heat_content/heat_content/heat_content_anomaly_0-700_pentad.nc
NOAA_OCEAN_PENTAD_HEAT_0_2000=/data/oceans/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/NETCDF/heat_content/heat_content_anomaly_0-2000_pentad.nc
NOAA_RATPAC_A=/pub/data/ratpac/ratpac-a/RATPAC-A-annual-levels.txt.zip
NOAA_DAILY_METHANE_BRW=/aftp/data/trace_gases/ch4/in-situ/surface/nc/ch4_brw_surface-insitu_1_ccgg_DailyData.nc
NOAA_DAILY_METHANE_MLO=/aftp/data/trace_gases/ch4/in-situ/surface/nc/ch4_mlo_surface-insitu_1_ccgg_DailyData.nc
NOAA_PALEO_VOSTOK_N2O=/pub/data/paleo/icecore/antarctica/vostok/vostok_n2o_iso.txt
NOAA_SOLAR_FLUX=/json/f107_cm_flux.json
NOAA_SUNSPOT=/json/solar-cycle/sunspots.json
NOAA_KP_INDEX=/json/planetary_k_index_1m.json
NOAA_ENSO_NINO34=/data/indices/ersst5.nino.mth.91-20.ascii
NOAA_CO2_MAUNA_LOA=/webdata/ccgg/trends/co2/co2_mm_mlo.csv

PELTIER_BASE_URL=https://www.atmosp.physics.utoronto.ca
PELTIER_DATA=/~peltier/datasets/Ice7G_NA_VM7/I7G_NA.VM7_1deg.26.nc.gz

```

<!-- END_ENV_EXAMPLE -->


## 📑 Кінцеві точки (Endpoints)

Доступні маршрути для отримання оброблених кліматичних даних:

  ```text
  constants/routes.py
  ```
<!-- START_ROUTES_TABLE -->

| Назва маршруту | URL / Шлях |
| :--- | :--- |
| **CH4NAT** | `/api/noaa/vostok/ch4nat` |
| **CO2NAT** | `/api/noaa/vostok/co2nat` |
| **CO2_MAUNA_LOA** | `/api/noaa/co2_mauna_loa` |
| **DUSTNAT** | `/api/noaa/vostok/dustnat` |
| **ENSO_NINO34** | `/api/noaa/enso_nio34` |
| **GISTEMP** | `/api/nasa/gistemp` |
| **GMSL** | `/api/nasa/gmsl` |
| **GMSL_INDICATOR** | `/api/nasa/gmsl_indicator` |
| **KP_INDEX** | `/api/noaa/kp_index` |
| **N2O_ISO** | `/api/noaa/vostok/n2o_iso` |
| **NASA** | `/api/nasa` |
| **NOAA** | `/api/noaa` |
| **NOAA_DAILY_METHANE_BRW** | `/api/noaa/daily_methane_brw` |
| **NOAA_DAILY_METHANE_MLO** | `/api/noaa/daily_methane_mlo` |
| **NOAA_RATPAC_A** | `/api/noaa/ratpac_a` |
| **NORTH_ICE** | `/api/noaa/north_ice_extent` |
| **OCEAN_PENTAD_HEAT_0_2000** | `/api/noaa/ocean_pentad_heat_0_2000` |
| **OCEAN_PENTAD_HEAT_0_700** | `/api/noaa/ocean_pentad_heat_0_700` |
| **OZONE** | `/api/nasa/ozone` |
| **PALEO_SEA_LEVEL** | `/api/noaa/paleo_sea_level` |
| **PELTIER** | `/api/peltier` |
| **RELATIVE_SEA_LEVEL** | `/api/noaa/relative_sea_level` |
| **RELATIVE_SEA_LEVEL_SUMMARY** | `/api/noaa/relative_sea_level_summary` |
| **SOLAR_FLUX** | `/api/noaa/solar_flux` |
| **SOUTH_ICE** | `/api/noaa/south_ice_extent` |
| **STRATOSPHERIC_AEROSOL** | `/api/nasa/stratospheric_aerosol` |
| **SUNSPOT** | `/api/noaa/sunpot` |
| **TEMP** | `/api/noaa/vostok/temp` |
| **VOSTOK** | `/api/noaa/vostok` |

<!-- END_ROUTES_TABLE -->


## 🏗 Структура проєкту

<!-- START_STRUCTURE_TREE -->

```tree
app/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── nasa/
│   │   ├── __init__.py
│   │   ├── gistemp/
│   │   │   ├── __init__.py
│   │   │   └── gistemp_parser.py
│   │   ├── gmsl/
│   │   │   ├── __init__.py
│   │   │   └── nc_nasa_parser.py
│   │   ├── gmsl_indicator/
│   │   │   ├── __init__.py
│   │   │   ├── calculate_index.py
│   │   │   └── gmsl_indicator_parser.py
│   │   ├── handler.py
│   │   ├── ozone/
│   │   │   ├── __init__.py
│   │   │   ├── fresh_link_generator.py
│   │   │   └── ozone_data_parser.py
│   │   ├── session.py
│   │   └── stratospheric_aerosol/
│   │       ├── __init__.py
│   │       └── stratospheric_aerosol_parser.py
│   ├── noaa/
│   │   ├── __init__.py
│   │   ├── co2_mauna_loa/
│   │   │   ├── __init__.py
│   │   │   └── co2_mauna_loa_parser.py
│   │   ├── enso_nio34/
│   │   │   ├── __init__.py
│   │   │   └── enso_nino34_parser.py
│   │   ├── handler.py
│   │   ├── methane/
│   │   │   ├── __init__.py
│   │   │   └── methane_parser.py
│   │   ├── noaa_ice_extent/
│   │   │   ├── __init__.py
│   │   │   └── noaa_ice_data_parser.py
│   │   ├── ocean_pentad_heat/
│   │   │   ├── __init__.py
│   │   │   └── ocean_pentad_heat_data.py
│   │   ├── paleo_sea_level/
│   │   │   ├── __init__.py
│   │   │   └── noaa_paleo_parser.py
│   │   ├── ratpac_a/
│   │   │   ├── __init__.py
│   │   │   └── ratpac_text_parser.py
│   │   ├── relative_sea_level/
│   │   │   ├── __init__.py
│   │   │   └── relative_sea_level_parser.py
│   │   ├── relative_sea_level_summary/
│   │   │   ├── __init__.py
│   │   │   └── relative_sea_level_summary_parser.py
│   │   ├── session.py
│   │   └── vostok/
│   │       ├── __init__.py
│   │       ├── ch4nat/
│   │       │   ├── __init__.py
│   │       │   └── vostok_ch4nat_parser.py
│   │       ├── co2nat/
│   │       │   ├── __init__.py
│   │       │   └── vostok_co2_nat_parser.py
│   │       ├── dustnat_noaa/
│   │       │   ├── __init__.py
│   │       │   └── dustnat_noaa_parser.py
│   │       ├── handler.py
│   │       ├── n2o_iso/
│   │       │   ├── __init__.py
│   │       │   └── n2o_iso_parser.py
│   │       └── temp/
│   │           ├── __init__.py
│   │           └── vostok_temp_parser.py
│   └── peltier/
│       ├── __init__.py
│       ├── handler.py
│       └── peltier_data_parser.py
├── constants/
│   ├── __init__.py
│   ├── blueprints_names.py
│   └── routes.py
└── helpers/
    ├── __init__.py
    ├── csv_converter.py
    ├── custom_json_provider.py
    ├── date_parsers.py
    ├── decompress_gz.py
    ├── extract_file_from_zip.py
    └── http_request.py
├── main.py
├── update_docs.py
├── .env
└── pyproject.toml
```

<!-- END_STRUCTURE_TREE -->