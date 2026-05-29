REGISTERED_ROUTE_CLASSES = []
FULL_ROUTES_FOR_README = []

# Декоратор, який автоматично реєструє класи для документації
def register_routes(cls):
    if cls not in REGISTERED_ROUTE_CLASSES:
        REGISTERED_ROUTE_CLASSES.append(cls)
    return cls

def with_prefix(prefix: str):
    def decorator(cls):
        for key, value in list(cls.__dict__.items()):
            if key.isupper() and isinstance(value, str):
                # Формуємо повний шлях
                full_path = f"{prefix.rstrip('/')}/{value.lstrip('/')}"
                
                # Додаємо пару (Назва, Повний_Шлях) у наш масив для генератора
                FULL_ROUTES_FOR_README.append((key, full_path))
        return cls
    return decorator

class BaseRoutes:
    API = "/api"

@register_routes
@with_prefix(f"{BaseRoutes.API}")
class ApiRoutes:
    NASA = "/nasa"
    NOAA = "/noaa"
    PELTIER = "/peltier"

@register_routes
@with_prefix(f"{BaseRoutes.API}{ApiRoutes.NOAA}")
class NoaaRoutes:
    NORTH_ICE = "/north_ice_extent"       # base url https://noaadata.apps.nsidc.org
    SOUTH_ICE = "/south_ice_extent"       # base url https://noaadata.apps.nsidc.org
    NOAA_DAILY_METHANE_BRW="/daily_methane_brw"      # base url https://gml.noaa.gov
    NOAA_DAILY_METHANE_MLO="/daily_methane_mlo"      # base url https://gml.noaa.gov
    PALEO_SEA_LEVEL = "/paleo_sea_level"        # base url https://www.ncei.noaa.gov
    RELATIVE_SEA_LEVEL = "/relative_sea_level"
    RELATIVE_SEA_LEVEL_SUMMARY = "/relative_sea_level_summary"
    OCEAN_PENTAD_HEAT_0_700 = "/ocean_pentad_heat_0_700"
    OCEAN_PENTAD_HEAT_0_2000 = "/ocean_pentad_heat_0_2000"
    NOAA_RATPAC_A = "/ratpac_a"
    VOSTOK = "/vostok"
    SOLAR_FLUX = "/solar_flux"
    SUNSPOT = "/sunpot"
    KP_INDEX = "/kp_index"
    ENSO_NINO34="/enso_nio34"
    CO2_MAUNA_LOA = "/co2_mauna_loa"

@register_routes
@with_prefix(f"{BaseRoutes.API}{ApiRoutes.NASA}")
class NasaRoutes:
    GMSL_INDICATOR = "/gmsl_indicator"
    GMSL = "/gmsl"
    OZONE = "/ozone"
    GISTEMP = "/gistemp"
    STRATOSPHERIC_AEROSOL="/stratospheric_aerosol"

@register_routes
@with_prefix(f"{BaseRoutes.API}{ApiRoutes.NOAA}{NoaaRoutes.VOSTOK}")
class VostokRoutes:
    CO2NAT = "/co2nat"
    TEMP = "/temp"
    CH4NAT = "/ch4nat"
    DUSTNAT = "/dustnat"
    N2O_ISO = "/n2o_iso"
    
# --- ГЕНЕРАТОР ТАБЛИЦІ ---

def generate_readme_table() -> str:
    """Генерує чистий Markdown-текст таблиці для README."""
    markdown_lines = ["| Назва маршруту | URL / Шлях |", "| :--- | :--- |"]
    
    # Сортуємо наш новий масив за назвою для красивого вигляду
    FULL_ROUTES_FOR_README.sort(key=lambda x: x[0])
    
    for key, value in FULL_ROUTES_FOR_README:
        markdown_lines.append(f"| **{key}** | `{value}` |")
        
    return "\n".join(markdown_lines)