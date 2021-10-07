import click
from flask import current_app, g
from flask.cli import with_appcontext
from .model import *


def check_db():
    model = get_db()
    click.echo(model.book.return_all_records())


def get_db():
    """Get database """
    # db_name = 'hw907.db'
    # db_url = _CONNECTION_STRING
    # if 'mongo_client' not in g:
    #     movies_mongo_client = pymongo.MongoClient(db_url)
    #     g.mongo_client = movies_mongo_client

    # if 'db' not in g:
    #     my_db: Database = getattr(g.mongo_client, db_name)
    #     g.db = my_db
    if "model" not in g:
        g.model = Model()
    return g.model


def close_db(e=None):
    """Closes db  connection"""
    client = g.pop('model', None)
    if client is not None:
        client.close()


@click.command('check-db')
@with_appcontext
def check_db_command():
    """Ge."""
    click.echo('Start checking db ')
    check_db()
    click.echo('Finish checking db.')


def init_app(app):
    app.cli.add_command(check_db_command)
    app.teardown_appcontext(close_db)
