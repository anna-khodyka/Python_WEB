from flask import (
    Flask,
    redirect,
    url_for,
    g,
    Blueprint,
    render_template,
    request,
    flash,
)
from datetime import datetime
import pathlib
from werkzeug.exceptions import abort

from .clean import CleanFolder

clean_bp = Blueprint("clean", __name__, url_prefix="/clean")


@clean_bp.route("/", methods=("GET", "POST"))
def clean():

    error = None
    message = ""

    if request.method == "POST":
        try:
            user_input = request.form["path"]
            path = pathlib.Path(user_input)
            CleanFolder().parse_folder(path)

        except Exception:
            error = "Указанная папка не существует"

        if error is not None:
            flash(error)
        else:
            message = "Your folder is parsed sucessfully"
        return render_template("clean/cleaner_result.html", message=message)

    return render_template("clean/cleaner.html")
