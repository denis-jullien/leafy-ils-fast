from fastapi.testclient import TestClient


def test_delete_unknown_circulation(client: TestClient) -> None:
    response = client.delete("/api/v1/circulations/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Circulation not found"


def test_delete_circulation(client: TestClient) -> None:
    # add family
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200
    # add member
    member_data = {"firstname": "firstname", "surname": "surname", "family_id": 1}
    response = client.post("/api/v1/members", json=member_data)
    assert response.status_code == 200
    # add book
    book_data = {"title": "title", "author": "author"}
    response = client.post("/api/v1/books", json=book_data)
    assert response.status_code == 200

    data = {"borrowed_date": "2019-12-04", "book_id": 1, "member_id": 1}
    response = client.post("/api/v1/circulations", json=data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.delete(f"/api/v1/circulations/{data_response["id"]}")
    assert response.status_code == 204
    assert response.content == b""
