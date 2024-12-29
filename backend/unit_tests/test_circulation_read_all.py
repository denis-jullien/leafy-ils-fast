from fastapi.testclient import TestClient
import pytest
from ..internals import constants


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
    total_items = 150
    for _ in range(total_items):
        response = client.post("/api/v1/circulations", json=init_data)
        assert response.status_code == 200
        circulation_list.append(response.json())

    # first page
    # Get All circulations with offset default: 0 and limit default: LIMIT_DEFAULT_VALUE
    limit = constants.LIMIT_DEFAULT_VALUE
    response = client.get("/api/v1/circulations")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for circulation in circulation_list[0:limit]:
        assert circulation in data_response
    # Get All books with page: 1 and limit: LIMIT_DEFAULT_VALUE
    page = 1
    limit = constants.LIMIT_DEFAULT_VALUE
    response = client.get(f"/api/v1/circulations?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for circulation in circulation_list[0:limit]:
        assert circulation in data_response

    # middle of pages
    # Get All circulations with page: 10 and limit: 6
    page = 10
    limit = 6
    offset = page * limit - limit
    response = client.get(f"/api/v1/circulations?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for circulation in circulation_list[offset : offset + limit]:
        assert circulation in data_response

    # last page
    # Get All circulations with page: 2 and limit: LIMIT_MAXIMAL_VALUE
    page = 2
    limit = constants.LIMIT_MAXIMAL_VALUE
    offset = page * limit - limit
    response = client.get(f"/api/v1/circulations?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) <= limit
    assert len(data_response) == total_items - offset
    for circulation in circulation_list[offset:total_items]:
        assert circulation in data_response


@pytest.mark.parametrize(
    "page,limit",
    [
        # invalid page
        (constants.PAGE_MINIMAL_VALUE - 1, 6),
        # invalid limit
        (1, constants.LIMIT_MINIMAL_VALUE - 1),
        (1, constants.LIMIT_MAXIMAL_VALUE + 1),
    ],
)
def test_read_all_circulation_with_pagination_failure(
    client: TestClient, page: int, limit: int
) -> None:
    response = client.get(f"/api/v1/circulations?page={page}&limit={limit}")
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response
