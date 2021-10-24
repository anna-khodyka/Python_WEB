'''предоставляет и закрывает доступ приложению к БД'''
import click
from flask import g
from flask.cli import with_appcontext
from .model import Model
from .db_classes import engine, session, Base


def check_db():
    '''проверяет есть ли доступ к БД'''
    get_db()
    click.echo("Initialized the database.")
    # click.echo(model.book.return_all_records())  # переписать на что=то другое


def get_db():
    """Get database"""

    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    if "model" not in g:
        g.model = Model(session)
    return g.model


def close_db(err=None):
    """Closes db  connection"""
    print(err)
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
    '''init and teardown the application'''
    app.cli.add_command(check_db_command)
    app.teardown_appcontext(close_db)
