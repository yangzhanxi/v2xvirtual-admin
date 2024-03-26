from flask import Flask

from services.authentication.auth_blueprint import auth as auth_bp
from services.license_management.license_blueprint import lic as lic_bp


def send_index(app: Flask):
    """
    Returns index.html.
    """
    return app.send_static_file("index.html")


def generate_routes(app: Flask) -> None:
    """
    Generate routes.

    :param app: Flask instance.
    """
    # Register authentication resource.
    app.register_blueprint(auth_bp, url_prefix="/api")

    # Register license resource.
    app.register_blueprint(lic_bp, url_prefix="/api")

    @app.route("/<path:filename>")
    def server_static(filename):
        return app.send_static_file(filename)

    @app.get("/")
    def index():
        return send_index(app)

    @app.get("/licenses")
    def licenses():
        return send_index(app)

    @app.get("/auth")
    def auth():
        return send_index(app)
