# NASA Climate Data Collector (GMSL)

Проєкт для автоматизації збору та обробки наукових даних NASA щодо глобального середнього рівня моря (**Global Mean Sea Level - GMSL**). Додаток реалізує повний цикл: від авторизації в захищених архівах NASA до парсингу бінарних NetCDF файлів.

## 🌟 Особливості
- **NASA Earthdata Integration**: Реалізовано складну логіку авторизації через `requests.Session` з підтримкою редиректів між доменами.
- **NetCDF4 Parsing**: Автоматичне витягування часових рядів та показників зміни рівня моря з бінарних наукових форматів.
- **Robust Architecture**: Модульна структура з чітким розділенням на обробники (handlers) та допоміжні інструменти (helpers).
- **Security First**: Використання змінних оточення для захисту облікових даних NASA.

## 🏗 Структура проєкту
```text
app/
├── helpers/             # Універсальні інструменти
│   ├── http_request.py  # Просунутий HTTP-клієнт з підтримкою сесій
│   └── date_parsers.py  # Обробка часових форматів
├── nasa/                # Логіка специфічна для NASA
│   └── gmsl/            # Обробка даних рівня моря
│       ├── handler.py   # Координація запитів та обробка помилок
│       └── nc_nasa_parser.py # Логіка розбору .nc файлів
├── main.py              # Точка входу Flask
└── .env                 # Конфігурація (не додається в Git)

# Облікові дані NASA Earthdata (URS)
NASA_USER=your_username
NASA_PASS=your_password

# Базовий URL архіву та посилання на дані
ARCHIVE_PODAAC_URL=[https://archive.podaac.earthdata.nasa.gov](https://archive.podaac.earthdata.nasa.gov)
NASA_SSH_GMSL_DATA_URL=/podaac-ops-cumulus-protected/JPL_RECON_GMSL/global_timeseries_measures.nc

python main.py