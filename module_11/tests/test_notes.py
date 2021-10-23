from helper.db import get_db
from helper.db_classes import Note


def test_index(client):
    response = client.get("/notes/")
    assert response.status_code == 200
    assert b"All notes" in response.data
    assert b"test text" in response.data
    assert b"test tag" in response.data


def test_add(client, app):
    assert client.get("/notes/add").status_code == 200
    response = client.post(
        "/notes/add",
        data={
            "note_tags": "to do list",
            "note_text": "do nothing",
            "created_at": "27.10.2021",
        },
        follow_redirects=True,
    )
    assert b"TO DO LIST" in response.data
    assert response.status_code == 200
    assert b"Edit" in response.data

    with app.app_context():
        db = get_db()
        assert db.session.query(Note).count() == 12
        new_record = db.session.query(Note).filter_by(id=12).one()
        assert new_record
        assert new_record.note_tags == "TO DO LIST"


def test_add_with_bad_created_at(client, app):
    response = client.post(
        "/notes/add",
        data={
            "note_tags": "wrong note",
            "note_text": "wrong text",
            "created_at": "27.102021",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Wrong date." in response.data


def test_add_with_empty_text(client, app):
    response = client.post(
        "/notes/add",
        data={"note_tags": "wrong note", "note_text": "", "created_at": "27.10.2021"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Note_text is required." in response.data


def test_find(client, app):
    response = client.post(
        "/notes/find", data={"keyword": "test tag"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"test tag" in response.data
    assert b"test text" in response.data


def test_sort(client, app):
    for i in "1234":
        response = client.post(
            "/notes/sort", data={"sort_type": i}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"test text" in response.data


def test_delete(client, app):
    response = client.post("/notes/12/delete", follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert not (b"TO DO LIST" in response.data)


def test_edit(client, app):
    response = client.get("/notes/1/edit")
    assert response.status_code == 200
    assert b"test text" in response.data

    response = client.post(
        "/notes/1/edit",
        data={
            "note_tags": "upd tag",
            "note_text": "test text",
            "created_at": "1980-06-12",
        },
        follow_redirects=True,
    )
    assert b"upd tag" in response.data
    assert response.status_code == 200
    assert b"Edit" in response.data

    response = client.post(
        "/notes/1/edit",
        data={
            "note_tags": "upd tag",
            "note_text": "test text",
            "created_at": "12.06.1975",
        },
        follow_redirects=True,
    )
    assert b"upd tag" in response.data
    assert response.status_code == 200
    assert b"Edit" in response.data


def test_edit_with_empty_text(client, app):
    response = client.post(
        "/notes/1/edit",
        data={"note_tags": "upd tag", "note_text": "", "created_at": "1980-06-12"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Text of note is required." in response.data


def test_edit_with_wrong_created_at(client, app):
    response = client.post(
        "/notes/1/edit",
        data={
            "note_tags": "upd tag",
            "note_text": "test text",
            "created_at": "1980-0612",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Wrong date." in response.data
