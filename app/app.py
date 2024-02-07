import os
import secrets

from flask import Flask

from routes import generate_routes


def create_app():
    """
    Create a flask APP.

    Returns:
        app: Returns the flask instance.
    """
    app = Flask(__name__)
    # App configuration
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", secrets.token_urlsafe())
    app.config["SECURITY_PASSWOR_SALT"] = os.environ.get(
        "SECURITY_PASSWORD_SALT", secrets.SystemRandom().getrandbits(128))

    generate_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run()
