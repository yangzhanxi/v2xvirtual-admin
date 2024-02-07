from flask import Blueprint
from flask_security import auth_required

auth = Blueprint("auth", __name__)


# @auth.route("/login", methods=["GET"])
@auth.post("/login")
def login():
    return "<p> LOGIN !</p>"


# @auth.route("/logout", methods=["GET"])
@auth.post("/logout")
@auth_required()
def logout():
    return "<p> LOG OUT !</p>"
