from fastapi.testclient import TestClient


def test_read_all_member_without_member(client: TestClient) -> None:
    response = client.get("/api/v1/members")
    assert response.status_code == 200
    data_response = response.json()
    assert data_response == []


def test_read_all_member_with_pagination(client: TestClient) -> None:
    # add family
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200
    # add members
    member_list = list()
    init_data = {
        "firstname": "firstname",
        "surname": "surname",
        "family_referent": True,
        "birthdate": "2019-12-04",
        "family_id": 1,
    }
    for _ in range(150):
        response = client.post("/api/v1/members", json=init_data)
        assert response.status_code == 200
        member_list.append(response.json())

    # Get All members with offset default: 0 and limit default: 100
    response = client.get("/api/v1/members")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 100
    for member in member_list[0:100]:
        assert member in data_response

    # Get All members with offset: 110 and limit: 10
    response = client.get("/api/v1/members?offset=110&limit=10")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 10
    for member in member_list[110:120]:
        assert member in data_response
