from helper.db import get_db
from helper.db_classes import Record


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"All contacts" in response.data
    assert b"test name" in response.data
    assert b"+380661112233" in response.data


# def test_add(client, app):
#     assert client.get('/add').status_code == 200
#     response = client.post(
#         '/add', data={'name': 'Anya', 'birthday': '12.031980', 'address': 'Bucha', "email": "anna@bigmir.net", "tags": "friends", "phone": "+380978440011"}, follow_redirects=True
#     )
#     assert b'Anya' in response.data
#     assert response.status_code == 200
#     with app.app_context():
#         assert get_db().session.query(Record).count() == 11
    # assert get_db().session.query(Record).filter_by(id=12).one()
