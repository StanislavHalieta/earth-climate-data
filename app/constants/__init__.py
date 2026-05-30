from .routes import (
    ApiRoutes,
    NoaaRoutes,
    NasaRoutes,
    BaseRoutes,
    VostokRoutes,
    generate_readme_table,
    register_routes,
    with_prefix,
    FULL_ROUTES_FOR_README,
)
from .blueprints_names import Blueprints

__all__ = [
    "generate_readme_table",
    "register_routes",
    "with_prefix",
    "ApiRoutes",
    "NoaaRoutes",
    "NasaRoutes",
    "BaseRoutes",
    "VostokRoutes",
    "Blueprints",
    "FULL_ROUTES_FOR_README",
]
