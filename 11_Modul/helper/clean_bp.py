from flask import Flask, redirect, url_for, g, Blueprint, render_template, request, flash
from datetime import datetime
import pathlib
from werkzeug.exceptions import abort

from .clean import CleanFolder

clean_bp = Blueprint('clean', __name__, url_prefix='/clean')


@clean_bp.route('/', methods=('GET', 'POST'))
def clean():

    error = None
    if request.method == 'POST':
        try:
            # сделать форму где поле имеет имя 'path'
            user_input = request.form['path']
            print(user_input)
            path = pathlib.Path(user_input)
            CleanFolder().print_recursive(path, user_input)
            CleanFolder().delete_dir(user_input)
        except Exception as er:
            error = er

        if error is not None:
            flash(error)

        return redirect(url_for('contact.index')) 

    return render_template('clean/cleaner.html')
