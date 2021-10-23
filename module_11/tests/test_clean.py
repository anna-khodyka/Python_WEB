def test_index(client):
    response = client.get("/clean/")
    assert response.status_code == 200
    assert b"Clean" in response.data

    response = client.post("/clean/", data={"path": "D:\Hlam"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your folder is parsed sucessfully" in response.data


def test_clean_nonexisted_path(client, app):
    response = client.post("/clean/", data={"path": "agaagg"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your folder is not existed" in response.data
