from helper.db import get_db
from helper.db_classes import Record


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"All contacts" in response.data
    assert b"test name" in response.data
    assert b"+380661112233" in response.data


def test_add(client, app):
    assert client.get("/add").status_code == 200
    response = client.post(
        "/add",
        data={
            "name": "Anya",
            "birthday": "12.03.1980",
            "address": "Bucha",
            "email": "anna@bigmir.net",
            "tags": "friends",
            "phone": "+380978440011",
        },
        follow_redirects=True,
    )
    assert b"Anya" in response.data
    assert response.status_code == 200
    assert b"Edit" in response.data

    with app.app_context():
        db = get_db()
        assert db.session.query(Record).count() == 12
        new_record = db.session.query(Record).filter_by(id=12).one()
        assert new_record
        assert new_record.name == "Anya"


def test_add_with_bad_birthday(client, app):
    response = client.post(
        "/add",
        data={
            "name": "Vasya",
            "birthday": "99.03.1980",
            "address": "Bucha",
            "email": "anna@bigmir.net",
            "tags": "friends",
            "phone": "+380978440011",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Wrong Birthday." in response.data


def test_add_with_bad_email(client, app):
    response = client.post(
        "/add",
        data={
            "name": "Vasya",
            "birthday": "01.03.1980",
            "address": "Bucha",
            "email": "annanetanna.bigmir.net",
            "tags": "friends",
            "phone": "+380978440011",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        b"Format is wrong. Try again in format: your_nickname@something.domen_name"
        in response.data
    )


def test_add_with_bad_address(client, app):
    response = client.post(
        "/add",
        data={
            "name": "Kolya",
            "birthday": "01.03.1980",
            "address": "BuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBuchaBucha",
            "email": "anna@bigmir.net",
            "tags": "friends",
            "phone": "+380978440011",
        },
        follow_redirects=True,
    )
    print(response.data)
    assert response.status_code == 200
    assert b"Please no more than 30 symbols" in response.data


def test_add_with_empty_name(client, app):
    response = client.post(
        "/add",
        data={
            "name": "",
            "birthday": "01.03.1980",
            "address": "Bucha",
            "email": "anna@bigmir.net",
            "tags": "friends",
            "phone": "+380978440011",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Name is required." in response.data


def test_add_with_bad_tags(client, app):
    response = client.post(
        "/add",
        data={
            "name": "Vasya",
            "birthday": "01.03.1980",
            "address": "Bucha",
            "email": "anna.bigmir.net",
            "tags": "friendsfriendsfriendsfriendsfriendsfriendsfriendsfriends",
            "phone": "+380978440011",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please no more than 15 symbols" in response.data


def test_add_with_bad_phone(client, app):
    response = client.post(
        "/add",
        data={
            "name": "Vasya",
            "birthday": "01.03.1980",
            "address": "Bucha",
            "email": "anna.bigmir.net",
            "tags": "friends",
            "phone": "38097844001155",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Phone may start with + and has from 3 to 12 digits max" in response.data


def test_find(client, app):
    response = client.post(
        "/find", data={"keyword": "test name"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"test address" in response.data
    assert b"+380661112233" in response.data


def test_sort(client, app):
    for i in "1234":
        response = client.post("/sort", data={"sort_type": i}, follow_redirects=True)
        assert response.status_code == 200
        assert b"test address" in response.data


def test_delete(client, app):

    response = client.post("/12/delete", follow_redirects=True)
    assert response.status_code == 200
    assert not (b"Anya" in response.data)

    # response = client.post(
    #     "/5555/delete", follow_redirects=True)
    # assert response.status_code == 400


def test_edit(client, app):
    response = client.get("/1/edit")
    assert response.status_code == 200
    assert b"test name" in response.data

    response = client.post(
        "/1/edit",
        data={
            "name": "upd name",
            "birthday": "1980-06-12",
            "address": "test address",
            "email": "test@test.ts",
            "tags": "test tag",
            "phone": "+380661112233",
        },
        follow_redirects=True,
    )
    assert b"upd name" in response.data
    assert response.status_code == 200
    assert b"Edit" in response.data


def test_edit_with_empty_name(client, app):
    response = client.post(
        "/1/edit",
        data={
            "name": "",
            "birthday": "12.06.1980",
            "address": "test address",
            "email": "test@test.ts",
            "tags": "test tag",
            "phone": "+380661112233",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Name is required." in response.data


def test_edit_with_bad_birthday(client, app):
    response = client.post(
        "/1/edit",
        data={
            "name": "upd name",
            "birthday": "99.06.1980",
            "address": "test address",
            "email": "test@test.ts",
            "tags": "test tag",
            "phone": "+380661112233",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Wrong Birthday." in response.data


def test_edit_with_bad_address(client, app):
    response = client.post(
        "/1/edit",
        data={
            "name": "upd name",
            "birthday": "12.06.1980",
            "address": "test address test address test address test address test address test address",
            "email": "test@test.ts",
            "tags": "test tag",
            "phone": "+380661112233",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please no more than 30 symbols" in response.data


def test_edit_with_bad_email(client, app):
    response = client.post(
        "/1/edit",
        data={
            "name": "upd name",
            "birthday": "12.06.1980",
            "address": "test address",
            "email": "test.test.ts",
            "tags": "test tag",
            "phone": "+380661112233",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        b"Format is wrong. Try again in format: your_nickname@something.domen_name"
        in response.data
    )


def test_edit_with_bad_tags(client, app):
    response = client.post(
        "/1/edit",
        data={
            "name": "upd name",
            "birthday": "12.06.1980",
            "address": "test address",
            "email": "test@test.ts",
            "tags": "test tag test tag test tag test tag test tag",
            "phone": "+380661112233",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Please no more than 15 symbols" in response.data


def test_edit_with_bad_phone(client, app):
    response = client.post(
        "/1/edit",
        data={
            "name": "upd name",
            "birthday": "12.06.1980",
            "address": "test address",
            "email": "test@test.ts",
            "tags": "test tag",
            "phone": "+38",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Phone may start with + and has from 3 to 12 digits max" in response.data
