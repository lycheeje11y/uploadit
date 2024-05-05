from flask import Blueprint

user_routes = Blueprint("users", __name__)

from . import login, logout, register, reset_password_request, reset_password