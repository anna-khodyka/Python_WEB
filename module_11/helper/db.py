import click
from flask import current_app, g
from flask.cli import with_appcontext
from .model import *


def check_db():
    model = get_db()
    click.echo('Initialized the database.')
    # click.echo(model.book.return_all_records())  # переписать на что=то другое


def get_db():
    """Get database"""
    db_name = current_app.config['DB_NAME']
    if "model" not in g:
        g.model = Model()
    return g.model


def close_db(e=None):
    """Closes db  connection"""
    client = g.pop("model", None)
    if client is not None:
        client.session.close()


@click.command("check-db")
@with_appcontext
def check_db_command():
    """Ge."""
    click.echo("Start checking db ")
    check_db()
    click.echo("Finish checking db.")


def init_app(app):
    app.cli.add_command(check_db_command)
    app.teardown_appcontext(close_db)
