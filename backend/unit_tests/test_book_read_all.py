from fastapi.testclient import TestClient
import pytest
from ..internals import constants


def test_read_all_book_without_book(client: TestClient) -> None:
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    data_response = response.json()
    assert data_response == []


def test_read_all_book_with_pagination(client: TestClient) -> None:
    book_list = list()
    init_data = {
        "title": "title",
        "author": "author",
        "abstract": "abstract",
        "publisher": "publisher",
        "catalog": "catalog",
        "category_type": "category_type",
        "category_age": "category_age",
        "category_topics": "category_topics",
        "language": "fr",
        "cover": "cover",
        "available": False,
        "archived": True,
    }
    total_items = 150
    for _ in range(total_items):
        response = client.post("/api/v1/books", json=init_data)
        assert response.status_code == 200
        book_list.append(response.json())

    # first page
    # Get All books with page default: 1 and limit default: LIMIT_DEFAULT_VALUE
    limit = constants.LIMIT_DEFAULT_VALUE
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for book in book_list[0:limit]:
        assert book in data_response
    # Get All books with page: 1 and limit: LIMIT_DEFAULT_VALUE
    page = 1
    limit = constants.LIMIT_DEFAULT_VALUE
    response = client.get(f"/api/v1/books?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for book in book_list[0:limit]:
        assert book in data_response

    # middle of pages
    # Get All books with page: 10 and limit: 6
    page = 10
    limit = 6
    offset = page * limit - limit
    response = client.get(f"/api/v1/books?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == limit
    for book in book_list[offset : offset + limit]:
        assert book in data_response

    # last page
    # Get All books with page: 2 and limit: LIMIT_MAXIMAL_VALUE
    page = 2
    limit = constants.LIMIT_MAXIMAL_VALUE
    offset = page * limit - limit
    response = client.get(f"/api/v1/books?page={page}&limit={limit}")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) <= limit
    assert len(data_response) == total_items - offset
    for book in book_list[offset:total_items]:
        assert book in data_response


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
def test_read_all_book_with_pagination_failure(
    client: TestClient, page: int, limit: int
) -> None:
    response = client.get(f"/api/v1/books?page={page}&limit={limit}")
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response
