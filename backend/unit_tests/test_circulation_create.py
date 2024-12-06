import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "data",
    [
        {"borrowed_date": "2019-12-04", "book_id": 1, "member_id": 2},
        {"borrowed_date": "2019-12-04", "book_id": 1, "member_id": 1, "returned_date": "2019-12-20"}
    ]
)
def test_create_circulation(client: TestClient, data: dict) -> None:
    # add family
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200
    # add members
    member_data = {"firstname": "firstname", "surname": "surname", "family_id": 1}
    response = client.post("/api/v1/members", json=member_data)
    assert response.status_code == 200
    response = client.post("/api/v1/members", json=member_data)
    assert response.status_code == 200
    # add book
    book_data = {"title": "title", "author": "author"}
    response = client.post("/api/v1/books", json=book_data)
    assert response.status_code == 200

    response = client.post("/api/v1/circulations", json=data)
    assert response.status_code == 200

    data_response = response.json()
    assert "id" in data_response
    for key, value in data.items():
        assert data_response[key] == value
