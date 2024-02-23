from flask import Flask

from services.authentication.auth_blueprint import auth as auth_bp
from services.license_management.license_bluprint import lic as lic_bp


def generate_routes(app: Flask) -> None:
    """
    Generate routes.

    :param app: Flask instance.
    """
    # Register authentication resource.
    app.register_blueprint(auth_bp, url_prefix="/api")

    # Register license resource.
    app.register_blueprint(lic_bp, url_prefix="/api")
