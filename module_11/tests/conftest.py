from itertools import chain
import os
import pathlib
import pytest
from faker import Faker
from flask import g

from helper import create_app
from helper.db import get_db
from helper.db_classes import *

fake = Faker()


def _init_db():
    """наполенение тестовой базы фейковыми данными"""
    # улучшить: добавить генерацию случайных телефонов, дат
    db = get_db()
    # наполнение таблицы Record и Note
    record = Record(
        name="test name",
        birthday=None,
        address="test address",
        email="test@test.ts",
        tags="test tag",
    )
    record.phones.append(Phone(phone_value="+380661112233"))
    db.session.add(record)
    db.session.add(Note(note_tags="test tag", note_text="test text", created_at=None))

    for _ in range(10):
        record = Record(
            name=fake.name(),
            birthday=None,
            address=fake.address(),
            email=fake.ascii_email(),
            tags="friends",
        )
        record.phones.append(Phone(phone_value="+380661524444"))
        db.session.add(record)
        db.session.add(
            Note(
                note_tags=fake.text(max_nb_chars=10),
                note_text=fake.text(max_nb_chars=30),
                created_at=None,
            )
        )
    db.session.commit()


@pytest.fixture(scope="module")
def app():
    # инициирует приложение
    app = create_app(
        {
            "TESTING": True,
            "DB_NAME": "test_db",
            "SECRET_KEY": b"test_secret",
        }
    )

    # создает тестовую БД
    with app.app_context():
        _init_db()

    yield app

    # удаляем тестовую БД после использования
    file = pathlib.Path(r"test.db")
    os.remove(file)


@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as client:
        return client


# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def runner(app):
#     return app.test_cli_runner()
