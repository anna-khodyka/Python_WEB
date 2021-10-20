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
from werkzeug.exceptions import abort

from .db import get_db

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


class InvalidRequestException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg


@notes_bp.route("/")
def index():
    model = get_db()
    notes_list = model.notes_book.all_notes()
    return render_template("notes/index.html", results=notes_list)


@notes_bp.route("/add", methods=("GET", "POST"))
def add():
    model = get_db()
    error = None
    if request.method == "POST":
        note_tags = request.form["note_tags"].upper()

        created_at = request.form["created_at"]
        if model.book.validate_birthday(created_at):
            created_at = datetime.strptime(created_at, "%d.%m.%Y").date()
        else:
            error = "Wrong date. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)"

        note_text = request.form["note_text"]
        if not note_text:
            error = "Note_text is required."

        if error is not None:
            flash(error)
        else:
            model.notes_book.add_note(
                text=note_text, hashtag=note_tags, created_at=created_at
            )
            return redirect(url_for("notes.index"))

    return render_template("notes/add.html")


@notes_bp.route("/<note_id>/delete", methods=("POST",))
def delete(note_id):
    try:
        model = get_db()
        model.notes_book.delete_note(note_id)
    except InvalidRequestException as e:
        abort(404, e.msg)
    return redirect(url_for("notes.index"))


@notes_bp.route("/<note_id>/edit", methods=("GET", "POST"))
def edit(note_id):
    model = get_db()
    error = None
    note = model.notes_book.find_note_for_editing(note_id)

    if request.method == "POST":

        note_text = request.form["note_text"]
        if not note_text:
            error = "Text of note is required."

        created_at = request.form["created_at"]
        if model.book.validate_birthday(created_at):
            created_at = datetime.strptime(created_at, "%d.%m.%Y").date()
        elif model.book.validate_birthday2(created_at):
            created_at = datetime.strptime(created_at, "%Y-%m-%d").date()
        else:
            error = "Wrong date. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)"

        note_tags = request.form["note_tags"]

        if error is not None:
            flash(error)
        else:
            model.notes_book.edit_note(
                id=note_id, new_text=note_text, new_hashtag=note_tags
            )
            return redirect(url_for("notes.index"))

    return render_template("notes/edit.html", note=note)


@notes_bp.route("/find", methods=("POST",))
def find():
    model = get_db()
    notes_list = model.notes_book.find_notes(request.form["keyword"])
    return render_template("notes/index.html", results=notes_list)


@notes_bp.route("/sort", methods=("POST",))
def sort():
    model = get_db()
    notes_list = model.notes_book.sort_notes(request.form["sort_type"])
    return render_template("notes/index.html", results=notes_list)
