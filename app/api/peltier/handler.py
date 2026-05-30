from dotenv import load_dotenv

from app.services import DatabaseService

from . import peltier_bp

load_dotenv()

db = DatabaseService()


@peltier_bp.route("/")
def get_peltier_home():
    return db.get_metric("peltier_data")
