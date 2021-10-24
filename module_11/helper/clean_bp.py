'''модуль инструмента по разбору хлама в папке, сортировке файлов по типам - Cleaner'''
import pathlib
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
)

from .clean import CleanFolder

clean_bp = Blueprint("clean", __name__, url_prefix="/clean")


@clean_bp.route("/", methods=("GET", "POST"))
def clean():
    '''handler инструмента по разбору хлама в папке, сортировке файлов по типам - Cleaner'''
    error = None
    message = ""

    if request.method == "POST":
        try:
            user_input = request.form["path"]
            path = pathlib.Path(user_input)
            CleanFolder().parse_folder(path)

        except ValueError as err:
            error = err

        if error is not None:
            flash(error)
        else:
            message = "Your folder is parsed sucessfully"
        return render_template("clean/cleaner_result.html", message=message)

    return render_template("clean/cleaner.html")
