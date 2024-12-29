from fastapi.testclient import TestClient
import pytest
from ..internals import constants


def test_read_all_family_without_family(client: TestClient) -> None:
    response = client.get("/api/v1/families")
    assert response.status_code == 200
    data_response = response.json()
    assert data_response == []


def test_read_all_family_with_pagination(client: TestClient) -> None:
    family_list = list()
    init_data = {"email": "test_email", "phone_number": "phone_test"}
    total_items = 150
    for _ in range(total_items):
        response = client.post("/api/v1/families", json=init_data)
        assert response.status_code == 200
        family_list.append(response.json())

    # Get All families with offset default: 0 and limit default: LIMIT_DEFAULT_VALUE
    limit = constants.LIMIT_DEFAULT_VALUE
    response = client.get("/api/v1/families")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for family in family_list[0:limit]:
        assert family in data_response
    # Get All families with page: 1 and limit: LIMIT_DEFAULT_VALUE
    page = 1
    limit = constants.LIMIT_DEFAULT_VALUE
    response = client.get(f"/api/v1/families?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for family in family_list[0:limit]:
        assert family in data_response

    # middle of pages
    # Get All families with page: 10 and limit: 6
    page = 10
    limit = 6
    offset = page * limit - limit
    response = client.get(f"/api/v1/families?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for family in family_list[offset : offset + limit]:
        assert family in data_response

    # last page
    # Get All families with page: 2 and limit: LIMIT_MAXIMAL_VALUE
    page = 2
    limit = constants.LIMIT_MAXIMAL_VALUE
    offset = page * limit - limit
    response = client.get(f"/api/v1/families?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) <= limit
    assert len(data_response) == total_items - offset
    for family in family_list[offset:total_items]:
        assert family in data_response


@pytest.mark.parametrize(
    "page,limit",
    [
        # invalid page
        (constants.DEFAULT_MINIMAL_VALUE - 1, 6),
        # invalid limit
        (1, constants.DEFAULT_MINIMAL_VALUE - 1),
        (1, constants.LIMIT_MAXIMAL_VALUE + 1),
    ],
)
def test_read_all_family_with_pagination_failure(
    client: TestClient, page: int, limit: int
) -> None:
    response = client.get(f"/api/v1/families?page={page}&limit={limit}")
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response
