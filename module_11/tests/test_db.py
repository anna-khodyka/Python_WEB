from helper.db import get_db
from flask import g
import pytest
import sqlite3

from helper.db_classes import Phone, Record, Note


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_model(app):
    with app.app_context():
        db = get_db()
        assert db is g.model


def test_get_users(app):
    with app.app_context():
        db = get_db()
        find_all_contacs = db.session.query(Record).count()
        find_all_notes = db.session.query(Note).count()
        find_all_phones = db.session.query(Phone).count()
        assert find_all_contacs == 11
        assert find_all_notes == 11
        assert find_all_phones == 11


def test_test_record_exists(app):
    with app.app_context():
        db = get_db()
        test_record = db.session.query(
            Record).filter_by(name='test name').one()
        assert test_record
        assert test_record.address == 'test address'
        assert test_record.email == 'test@test.ts'
        assert test_record.birthday == None
        assert test_record.tags == "test tag"
        assert test_record.phones[0].phone_value == "+380661112233"


def test_test_phone_exists(app):
    with app.app_context():
        db = get_db()
        test_phone = db.session.query(
            Phone).filter_by(phone_value="+380661112233").one()
        assert test_phone
        assert test_phone.phone_value == "+380661112233"


def test_test_note_exists(app):
    with app.app_context():
        db = get_db()
        test_note = db.session.query(
            Note).filter_by(note_tags='test tag').one()
        assert test_note
        assert test_note.note_tags == 'test tag'
        assert test_note.note_text == 'test text'
        assert test_note.created_at == None
