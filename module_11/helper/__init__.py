"""Helper module"""
import os

from flask import Flask
from . import db
from . import contact_bp
from . import clean_bp
from . import notes_bp


def create_app(test_config=None):
    '''create and configure the app'''
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping()
    app.config.from_mapping(SECRET_KEY="dev", DB_NAME="hw907")
    directory_path = os.getcwd()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        # DO not do this on prod
        app.config.from_pyfile(os.path.join(
            directory_path, "config.py"), silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(contact_bp.contact_bp)
    app.register_blueprint(clean_bp.clean_bp)
    app.register_blueprint(notes_bp.notes_bp)
    app.add_url_rule("/", endpoint="index")

    return app


# инструкция по запуску приложения
# $env:FLASK_APP = "helper"
# $env:FLASK_ENV="development"
# $env:MY_DB_NAME = "sqlite:///hw907.db"

# flask run
