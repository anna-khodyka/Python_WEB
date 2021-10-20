from helper.db import get_db


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"All contacts" in response.data
    assert b"test name" in response.data
    assert b"+380661112233" in response.data
