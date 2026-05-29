from app.constants import VostokRoutes
from app.api.noaa.vostok import vostok_bp

# Імпортуємо наш універсальний клас сервісу бази даних
from app.services import DatabaseService

# Ініціалізуємо об'єкт сервісу
db = DatabaseService()

@vostok_bp.route("/")
def get_vostok_home():
    return "Vostok home"

@vostok_bp.route(VostokRoutes.CO2NAT, methods=["GET"])
def get_vostok_co2_data():
    return db.get_metric("vostok_co2nat")

@vostok_bp.route(VostokRoutes.TEMP, methods=["GET"])
def get_vostok_temp_data():
    return db.get_metric("vostok_temp")

@vostok_bp.route(VostokRoutes.CH4NAT, methods=["GET"])
def get_vostok_ch4_data():
    return db.get_metric("vostok_ch4nat")

@vostok_bp.route(VostokRoutes.DUSTNAT, methods=["GET"])
def get_vostok_dust_data():
    return db.get_metric("vostok_dustnat")

@vostok_bp.route(VostokRoutes.N2O_ISO, methods=["GET"])
def get_vostok_n2o_iso_data():
    return db.get_metric("vostok_n2o_iso")
