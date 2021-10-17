from flask import Flask, redirect, url_for, g, Blueprint, render_template, request, flash
from datetime import datetime
from werkzeug.exceptions import abort

from .db import get_db

contact_bp = Blueprint('contact', __name__)


class InvalidRequestException(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg


@contact_bp.route('/')
def index():
    model = get_db()
    records_list = model.book.return_all_records()
    return render_template('contact/index.html', results=records_list)


@contact_bp.route('/find', methods=('POST',))
def find():
    model = get_db()
    records_list = model.book.find_value(request.form['keyword'])
    return render_template('contact/index.html', results=records_list)


@contact_bp.route('/sort', methods=('POST',))
def sort():
    model = get_db()
    records_list = model.book.sort(request.form['sort_type'])
    return render_template('contact/index.html', results=records_list)


@contact_bp.route('/add', methods=('GET', 'POST'))
def add():
    model = get_db()
    error = None
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            error = 'Name is required.'

        birthday = request.form['birthday']
        if model.book.validate_birthday(birthday):
            birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
        else:
            error = 'Wrong Birthday. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)'

        address = request.form['address']
        if address:
            if not model.book.validate_address(address):
                error = 'Your Address is {len(address)} symbols. Please no more than 30 symbols'
                address = None

        email = request.form['email']
        if email:
            if not model.book.validate_email_format(email):
                error = "Format is wrong. Try again in format: your_nickname@something.domen_name"
                email = None

        tags = request.form['tags']
        if tags:
            if not model.book.validate_tags(tags):
                error = 'Your Tags is {len(tags)} symbols. Please no more than 15 symbols'
                tags = None

        phone = request.form['phone']
        phones = []
        if phone:
            if not model.book.validate_phone(phone):
                error = 'Wrong input! Phone may start with + and has from 3 to 12 digits max. Example +380501234567'
            else:
                phones.append(phone)

        if error is not None:
            flash(error)
        else:
            model.book.add_record(
                name=name, birthday=birthday, address=address, email=email, tags=tags, phones=phones)
            return redirect(url_for('contact.index'))

    return render_template('contact/add.html')


@contact_bp.route('/<record_id>/delete', methods=('POST',))
def delete(record_id):
    try:
        model = get_db()
        model.book.remove_record(record_id)
    except InvalidRequestException as e:
        abort(404, e.msg)
    return redirect(url_for('contact.index'))


@contact_bp.route('/<record_id>/edit', methods=('GET', 'POST'))
def edit(record_id):
    model = get_db()
    error = None
    record = model.book.find_record(record_id)

    if request.method == 'POST':

        name = request.form['name']
        if not name:
            error = 'Name is required.'

        birthday = request.form['birthday']
        if model.book.validate_birthday(birthday):
            birthday = datetime.strptime(birthday, "%d.%m.%Y").date()
        elif model.book.validate_birthday2(birthday):
            birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
        else:
            error = 'Wrong Birthday. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)'

        address = request.form['address']
        if address:
            if not model.book.validate_address(address):
                error = 'Your Address is {len(address)} symbols. Please no more than 30 symbols'
                address = None

        email = request.form['email']
        if email:
            if not model.book.validate_email_format(email):
                error = "Format is wrong. Try again in format: your_nickname@something.domen_name"
                email = None

        tags = request.form['tags']
        if tags:
            if not model.book.validate_tags(tags):
                error = 'Your Tags is {len(tags)} symbols. Please no more than 15 symbols'
                tags = None

        phone = request.form['phone']
        if phone:
            if not model.book.validate_phone(phone):
                error = 'Wrong input! Phone may start with + and has from 3 to 12 digits max. Example +380501234567'

        if error is not None:
            flash(error)
        else:
            model.book.edit_record(
                record_id, name, birthday, address, email, tags, phone)
            return redirect(url_for('contact.index'))

    return render_template('contact/edit.html', record=record)
