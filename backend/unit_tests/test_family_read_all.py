from fastapi.testclient import TestClient


def test_read_all_family_without_family(client: TestClient) -> None:
    response = client.get("/api/v1/families")
    assert response.status_code == 200
    data_response = response.json()
    assert data_response == []


def test_read_all_family_with_pagination(client: TestClient) -> None:
    family_list = list()
    init_data = {"email": "test_email", "phone_number": "phone_test"}
    for _ in range(150):
        response = client.post("/api/v1/families", json=init_data)
        assert response.status_code == 200
        family_list.append(response.json())

    # Get All families with offset default: 0 and limit default: 100
    response = client.get("/api/v1/families")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 100
    for family in family_list[0:100]:
        assert family in data_response

    # Get All families with offset: 110 and limit: 10
    response = client.get("/api/v1/families?offset=110&limit=10")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 10
    for family in family_list[110:120]:
        assert family in data_response
