from fastapi.testclient import TestClient
import pytest


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
    total_items = 150
    for _ in range(total_items):
        response = client.post("/api/v1/members", json=init_data)
        assert response.status_code == 200
        member_list.append(response.json())

    # Get All members with offset default: 0 and limit default: 20
    limit = 20
    response = client.get("/api/v1/members")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for member in member_list[0:limit]:
        assert member in data_response
    # Get All members with page: 1 and limit: 20
    page = 1
    limit = 20
    response = client.get(f"/api/v1/members?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for member in member_list[0:limit]:
        assert member in data_response

    # middle of pages
    # Get All members with page: 10 and limit: 6
    page = 10
    limit = 6
    offset = page * limit - limit
    response = client.get(f"/api/v1/members?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for member in member_list[offset : offset + limit]:
        assert member in data_response

    # last page
    # Get All members with page: 2 and limit: 100
    page = 2
    limit = 100
    offset = page * limit - limit
    response = client.get(f"/api/v1/members?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) <= limit
    assert len(data_response) == total_items - offset
    for member in member_list[offset:total_items]:
        assert member in data_response


@pytest.mark.parametrize(
    "page,limit",
    [
        # invalid page
        (-1, 6),
        (0, 6),
        # invalid limit
        (1, 0),
        (1, -1),
        (1, 101),
    ],
)
def test_read_all_member_with_pagination_failure(
    client: TestClient, page: int, limit: int
) -> None:
    response = client.get(f"/api/v1/members?page={page}&limit={limit}")
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response
