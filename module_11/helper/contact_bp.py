'''модуль для работы с контактами и классами Record Phone'''
from datetime import datetime
from flask import (
    redirect,
    url_for,
    Blueprint,
    render_template,
    request,
    flash,
)
from werkzeug.exceptions import abort

from .db import get_db

contact_bp = Blueprint("contact", __name__)


class InvalidRequestException(Exception):
    '''класс для обработки ошибок'''

    def __init__(self, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg


@contact_bp.route("/")
def index():
    '''handler главной страницы с перечнем всех контактов'''
    model = get_db()
    records_list = model.book.return_all_records()
    return render_template("contact/index.html", results=records_list)


@contact_bp.route("/find", methods=("POST",))
def find():
    '''handler для поиска контакта'''
    model = get_db()
    records_list = model.book.find_value(request.form["keyword"])
    return render_template("contact/index.html", results=records_list)


@contact_bp.route("/sort", methods=("POST",))
def sort():
    '''handler сортировки контактов'''
    model = get_db()
    records_list = model.book.sort(request.form["sort_type"])
    return render_template("contact/index.html", results=records_list)


@contact_bp.route("/add", methods=("GET", "POST"))
def add():
    '''handler для добавления контакта'''
    model = get_db()
    error = None
    if request.method == "POST":
        name = request.form["name"]
        if not name:
            error = "Name is required."

        birthday = request.form["birthday"]
        if model.book.validate_birthday(birthday):
            birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
        else:
            error = "Wrong Birthday. Expected format: dd.mm.yyyy (example:25.12.1970)"

        address = request.form["address"]
        if address and not model.book.validate_address(address):
            error = "Your Address is {len(address)} symbols. Please no more than 30 symbols"
            address = None

        email = request.form["email"]
        if email and not model.book.validate_email_format(email):
            error = "Format is wrong. Try again in format: your_nickname@something.domen_name"
            email = None

        tags = request.form["tags"]
        if tags and not model.book.validate_tags(tags):
            error = (
                "Your Tags is {len(tags)} symbols: no more 15 symbols"
            )
            tags = None

        phone = request.form["phone"]
        phones = []
        if phone:
            if not model.book.validate_phone(phone):
                error = "Phone must contain 3-12 digits and can start with +. Example +380501234567"
            else:
                phones.append(phone)

        if error is not None:
            flash(error)
        else:
            model.book.add_record(
                name=name,
                birthday=birthday,
                address=address,
                email=email,
                tags=tags,
                phones=phones,
            )
            return redirect(url_for("contact.index"))

    return render_template("contact/add.html")


@contact_bp.route("/<record_id>/delete", methods=("POST",))
def delete(record_id):
    '''handler для удаления контакта'''
    try:
        model = get_db()
        model.book.remove_record(record_id)
    except InvalidRequestException as error:
        abort(400, error.msg)
    return redirect(url_for("contact.index"))


@contact_bp.route("/<record_id>/edit", methods=("GET", "POST"))
def edit(record_id):
    '''handler для редактирования контакта'''
    model = get_db()
    error = None
    record = model.book.find_record(record_id)

    if request.method == "POST":

        name = request.form["name"]
        if not name:
            error = "Name is required."

        birthday = request.form["birthday"]
        if model.book.validate_birthday(birthday):
            birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
        elif model.book.validate_birthday2(birthday):
            birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
        else:
            error = "Wrong Birthday. Expected format: dd.mm.yyyy (example:25.12.1970)"

        address = request.form["address"]
        if address and not model.book.validate_address(address):
            error = "Your Address is {len(address)} symbols. Please no more than 30 symbols"
            address = None

        email = request.form["email"]
        if email and not model.book.validate_email_format(email):
            error = "Format is wrong. Try again in format: your_nickname@something.domen_name"
            email = None

        tags = request.form["tags"]
        if tags and not model.book.validate_tags(tags):
            error = (
                "Your Tags is {len(tags)} symbols: no more 15 symbols"
            )
            tags = None

        phone = request.form["phone"]
        if phone and not model.book.validate_phone(phone):
            error = "Phone must contain 3-12 digits and can start with +. Example +380501234567"

        if error is not None:
            flash(error)
        else:
            model.book.edit_record(
                record_id, name, birthday, address, email, tags, phone
            )
            return redirect(url_for("contact.index"))

    return render_template("contact/edit.html", record=record)
