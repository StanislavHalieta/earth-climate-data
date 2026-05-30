from flask import Blueprint

from app.constants import Blueprints, BaseRoutes

from app.api.nasa import nasa_bp
from app.api.noaa import noaa_bp
from app.api.peltier import peltier_bp

api_bp = Blueprint(Blueprints.API, __name__, url_prefix=BaseRoutes.API)

api_bp.register_blueprint(noaa_bp)
api_bp.register_blueprint(nasa_bp)
api_bp.register_blueprint(peltier_bp)


__all__ = ["api_bp"]
