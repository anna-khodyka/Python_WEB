from itertools import chain

import pytest
from faker import Faker
from flask import g

from 11_MODUL.helper import create_app
from 11_MODUL.helper.db import get_db
from 11_MODUL.helper.db_classes import *
fake = Faker()


def _init_db():
    '''наполенение тестовой базы фейковыми данными'''
    db = get_db()
    # наполнение таблицы Record и Note
    for _ in range(10):
        record = Record(name=fake.name(), birthday=fake.date(),
                        address=fake.address(), email=fake.ascii_email(), tags="friends")
        # добавить генерацию случайных телефонов
        record.phones.append(Phone(phone_value="+380661524444"))
        db.session.add(record)
        db.session.add(Note(note_tags=fake.text(max_nb_chars=10),
                    note_text=fake.text(max_nb_chars=30), created_at=fake.date()))
        db.session.commit()


@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
        'DB_NAME': 'test_db',
        'SECRET_KEY': b'test_secret',
    })

    with app.app_context():
        _init_db()

    yield app

    # удаляем тестовую БД после использования
    with app.app_context():
        get_db()
        # g.mongo_client.drop_database(app.config['DB_NAME'])
        # g.model.???
