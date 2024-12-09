from fastapi.testclient import TestClient


def test_read_all_circulation_without_circulation(client: TestClient) -> None:
    response = client.get("/api/v1/circulations")
    assert response.status_code == 200
    data_response = response.json()
    assert data_response == []


def test_read_all_circulation_with_pagination(client: TestClient) -> None:
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
    # add circulations
    circulation_list = list()
    init_data = {
        "borrowed_date": "2022-12-04",
        "book_id": 1,
        "member_id": 1,
        "returned_date": "2030-12-20",
    }
    for _ in range(150):
        response = client.post("/api/v1/circulations", json=init_data)
        assert response.status_code == 200
        circulation_list.append(response.json())

    # Get All circulations with offset default: 0 and limit default: 100
    response = client.get("/api/v1/circulations")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 100
    for circulation in circulation_list[0:100]:
        assert circulation in data_response

    # Get All circulations with offset: 110 and limit: 10
    response = client.get("/api/v1/circulations?offset=110&limit=10")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 10
    for circulation in circulation_list[110:120]:
        assert circulation in data_response
