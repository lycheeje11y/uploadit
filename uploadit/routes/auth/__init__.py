from flask import Blueprint

auth = Blueprint("auth", __name__)

from . import login, logout, register, reset_password_request, reset_password