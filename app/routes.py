from flask import Flask, send_from_directory

from services.authentication.auth_blueprint import auth as auth_bp
from services.license_management.license_blueprint import lic as lic_bp


def generate_routes(app: Flask) -> None:
    """
    Generate routes.

    :param app: Flask instance.
    """
    # Register authentication resource.
    app.register_blueprint(auth_bp, url_prefix="/api")

    # Register license resource.
    app.register_blueprint(lic_bp, url_prefix="/api")

    @app.get("/<path:filename>")
    def server_static(filename):
        return send_from_directory(app.static_folder, filename)

    @app.get("/")
    def index():
        return send_from_directory(app.template_folder, "index.html")
