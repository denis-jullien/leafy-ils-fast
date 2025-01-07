from fastapi.testclient import TestClient
import pytest
from ..internals import constants


def add_a_lot_of_elements(
    client: TestClient, total_items: int, update_init_data: dict = None
):
    """
    default precondition for paginate API

    Return
    ----------
    book list
    """
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
    if update_init_data:
        for key, value in update_init_data.items():
            init_data[key] = value

    # create a lot of elements
    for _ in range(total_items):
        response = client.post("/api/v1/books", json=init_data)
        assert response.status_code == 200
        book_list.append(response.json())

    # provide the data to the test
    return book_list


def get_all_books_filtered(client: TestClient, filter: str) -> list:
    data_response = list()
    page = 1
    while True:
        response = client.get(f"/api/v1/books?page={page}&{filter}")
        assert response.status_code == 200
        list_response = response.json()
        assert "data" in list_response

        # exit the loop when the last page is reached
        if list_response["data"] == []:
            break
        data_response.extend(list_response["data"])
        page += 1
    return data_response


def test_read_all_book_without_book(client: TestClient) -> None:
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    list_response = response.json()
    assert "data" in list_response
    data_response = list_response["data"]
    assert data_response == []


# Get all elements with default queries
def test_read_all_book_with_pagination_default(client: TestClient) -> None:
    total_items = 150
    book_list = add_a_lot_of_elements(client, total_items)

    response = client.get("/api/v1/books")
    assert response.status_code == 200
    list_response = response.json()

    # first page
    limit = constants.LIMIT_DEFAULT_VALUE
    # data check
    assert "data" in list_response
    data_response = list_response["data"]
    assert len(data_response) == limit
    for book in book_list[0:limit]:
        assert book in data_response
    # meta check
    assert "meta" in list_response
    assert list_response["meta"]["total_items"] == total_items
    assert list_response["meta"]["total_pages"] == 8


@pytest.mark.parametrize(
    "input,output",
    [
        (
            {"page": 1, "limit": constants.LIMIT_DEFAULT_VALUE},
            {"count": constants.LIMIT_DEFAULT_VALUE, "total_pages": 8},
        ),
        ({"page": 10, "limit": 6}, {"count": 6, "total_pages": 25}),
        (
            {"page": 2, "limit": constants.LIMIT_MAXIMAL_VALUE},
            {"count": 50, "total_pages": 2},
        ),  # count = total_items - limit
    ],
)
# Get all elements with different queries
def test_read_all_book_with_pagination(
    client: TestClient, input: dict, output: dict
) -> None:
    total_items = 150
    page = input["page"]
    limit = input["limit"]
    count = output["count"]
    total_pages = output["total_pages"]
    offset = (page - 1) * limit
    book_list = add_a_lot_of_elements(client, total_items)

    response = client.get(f"/api/v1/books?page={page}&limit={limit}")
    assert response.status_code == 200
    list_response = response.json()

    # data check
    assert "data" in list_response
    data_response = list_response["data"]

    assert len(data_response) == count
    book_max = offset + limit if (offset + limit) < total_items else total_items
    for book in book_list[offset:book_max]:
        assert book in data_response

    # meta check
    assert "meta" in list_response
    assert list_response["meta"]["total_items"] == total_items
    assert list_response["meta"]["total_pages"] == total_pages


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
def test_read_all_book_with_pagination_failure(
    client: TestClient, page: int, limit: int
) -> None:
    response = client.get(f"/api/v1/books?page={page}&limit={limit}")
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response


@pytest.mark.parametrize(
    "archived_count,not_archived_count",
    [
        (17, 0),
        (0, 12),
        (152, 120),
    ],
)
def test_read_all_book_filtered_by_archived(
    client: TestClient, archived_count: int, not_archived_count: int
) -> None:
    book_list_archived = add_a_lot_of_elements(
        client, archived_count, {"archived": True}
    )
    book_list_not_archived = add_a_lot_of_elements(
        client, not_archived_count, {"archived": False}
    )
    book_list_archived.extend(
        add_a_lot_of_elements(client, archived_count, {"archived": True})
    )

    # Get all data with the filter

    current_book_list_archived = get_all_books_filtered(client, "filter[archived]=True")
    assert len(current_book_list_archived) == (archived_count * 2)
    assert current_book_list_archived == book_list_archived

    current_book_list_not_archived = get_all_books_filtered(
        client, "filter[archived]=False"
    )
    assert len(current_book_list_not_archived) == not_archived_count
    assert current_book_list_not_archived == book_list_not_archived


@pytest.mark.parametrize(
    "available_count,not_available_count",
    [
        (10, 0),
        (0, 120),
        (15, 120),
    ],
)
def test_read_all_book_filtered_by_available(
    client: TestClient, available_count: int, not_available_count: int
) -> None:
    book_list_available = add_a_lot_of_elements(
        client, available_count, {"available": True}
    )
    book_list_not_available = add_a_lot_of_elements(
        client, not_available_count, {"available": False}
    )
    book_list_available.extend(
        add_a_lot_of_elements(client, available_count, {"available": True})
    )

    # Get all data with the filter

    current_book_list_available = get_all_books_filtered(
        client, "filter[available]=True"
    )
    assert len(current_book_list_available) == (available_count * 2)
    assert current_book_list_available == book_list_available

    current_book_list_not_available = get_all_books_filtered(
        client, "filter[available]=False"
    )
    assert len(current_book_list_not_available) == not_available_count
    assert current_book_list_not_available == book_list_not_available
