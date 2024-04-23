from flask import Blueprint

home_page = Blueprint("Home Page", __name__)


@home_page.route("/", defaults={"path": None})
@home_page.route("/<path:path>")
def index(path, config):
    if path:
        requested_path = config.base_directory.joinpath(path)
        if str(requested_path) in config.available_files:
            return "returning"
        else:
            return "no path"
