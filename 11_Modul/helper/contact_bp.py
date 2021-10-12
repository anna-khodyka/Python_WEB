from flask import Flask, redirect, url_for, g, Blueprint, render_template

from .db import get_db

contact_bp = Blueprint('contact', __name__, url_prefix='/contact')


@contact_bp.route('/show')
def show():
    # return "Show results"
    # number = view.enter_number_of_page()
    number = 5
    model = get_db()
    records_list = model.book.return_all_records()
    # iter = model.book.iterator(records_list, number)
    # result = ""
    # for i in iter:
    #     result += i
    # result += "The end of the contacts book"
    return render_template('contact/index.html', results=records_list)
    # return render_template('contact/index.html', results=result)
    # return result
