from flask import Blueprint

from app.constants import (Blueprints, ApiRoutes)

from app.api.nasa.session import create_nasa_session

nasa_bp = Blueprint(Blueprints.NASA, __name__, url_prefix=ApiRoutes.NASA)

from . import handler

__all__ = ["nasa_bp", "create_nasa_session"]