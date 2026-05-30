from flask import Blueprint

from app.constants.blueprints_names import Blueprints
from app.constants.routes import ApiRoutes
from app.api.peltier.peltier_data_parser import parse_ns_peltier_data

peltier_bp = Blueprint(Blueprints.PELTIER, __name__, url_prefix=ApiRoutes.PELTIER)

from . import handler

__all__ = ["peltier_bp", "parse_ns_peltier_data"]
