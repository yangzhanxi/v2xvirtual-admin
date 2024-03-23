import os
import secrets
from datetime import timedelta

from flask import Flask, helpers
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_security import Security

from const import SECURITY_PASSWORD_SALT
from database.datastore import create_admin_role_and_user, init_datastore
from logging_module import config_log
from routes import generate_routes


def create_app() -> Flask:
    """
    Create a flask APP.

    :return: app: Returns the flask instance.
    """

    # Logging configuration
    config_log(helpers.get_debug_flag())

    app = Flask(__name__)

    app = Flask(__name__, static_folder="./dist/",
                template_folder="./dist/")
    CORS(app)

    # App configuration
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", secrets.token_urlsafe())

    app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
        "SECURITY_PASSWORD_SALT", SECURITY_PASSWORD_SALT)

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
    app.config["JWT_SECRET_KEY"] = secrets.token_urlsafe()

    user_datastore = init_datastore()

    setattr(app, "security", Security(app, user_datastore))

    create_admin_role_and_user(app)

    generate_routes(app)

    JWTManager(app)

    return app


if __name__ == "__main__":
    app = create_app()

    app.run()
