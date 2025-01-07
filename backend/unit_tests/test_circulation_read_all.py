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
    circulation list
    """
    # add family
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200
    # add members
    member_data = {"firstname": "firstname", "surname": "surname", "family_id": 1}
    response = client.post("/api/v1/members", json=member_data)
    assert response.status_code == 200
    member_id = response.json()["id"]
    response = client.post("/api/v1/members", json=member_data)
    assert response.status_code == 200
    # add book
    book_data = {"title": "title", "author": "author"}
    response = client.post("/api/v1/books", json=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]
    # add circulations
    circulation_list = list()
    init_data = {
        "borrowed_date": "2022-12-04",
        "book_id": book_id,
        "member_id": member_id,
        "returned_date": "2030-12-20",
    }
    if update_init_data:
        for key, value in update_init_data.items():
            init_data[key] = value

    # create a lot of elements
    for _ in range(total_items):
        response = client.post("/api/v1/circulations", json=init_data)
        assert response.status_code == 200
        circulation_list.append(response.json())

    # provide the data to the test
    return circulation_list


def get_all_circulations_filtered(client: TestClient, filter: str) -> list:
    data_response = list()
    page = 1
    while True:
        response = client.get(f"/api/v1/circulations?page={page}&{filter}")
        assert response.status_code == 200
        list_response = response.json()
        assert "data" in list_response

        # exit the loop when the last page is reached
        if list_response["data"] == []:
            break
        data_response.extend(list_response["data"])
        page += 1
    return data_response


def test_read_all_circulation_without_circulation(client: TestClient) -> None:
    response = client.get("/api/v1/circulations")
    assert response.status_code == 200
    list_response = response.json()
    assert "data" in list_response
    data_response = list_response["data"]
    assert data_response == []


def test_read_all_circulation_with_pagination_default(client: TestClient) -> None:
    total_items = 150
    circulation_list = add_a_lot_of_elements(client, total_items)

    response = client.get("/api/v1/circulations")
    assert response.status_code == 200
    list_response = response.json()

    # first page
    limit = constants.LIMIT_DEFAULT_VALUE
    # data check
    assert "data" in list_response
    data_response = list_response["data"]
    assert len(data_response) == limit
    for circulation in circulation_list[0:limit]:
        assert circulation in data_response
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
# Get All circulations with different queries
def test_read_all_circulation_with_pagination(
    client: TestClient, input: dict, output: dict
) -> None:
    total_items = 150
    page = input["page"]
    limit = input["limit"]
    count = output["count"]
    total_pages = output["total_pages"]
    offset = (page - 1) * limit
    circulation_list = add_a_lot_of_elements(client, total_items)

    response = client.get(f"/api/v1/circulations?page={page}&limit={limit}")
    assert response.status_code == 200
    list_response = response.json()

    # data check
    assert "data" in list_response
    data_response = list_response["data"]

    assert len(data_response) == count
    circulation_max = offset + limit if (offset + limit) < total_items else total_items
    for circulation in circulation_list[offset:circulation_max]:
        assert circulation in data_response

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
def test_read_all_circulation_with_pagination_failure(
    client: TestClient, page: int, limit: int
) -> None:
    response = client.get(f"/api/v1/circulations?page={page}&limit={limit}")
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response


def test_read_all_circulation_filtered_by_borrowed_date(client: TestClient) -> None:
    circulation_list_1 = add_a_lot_of_elements(
        client, 1, {"borrowed_date": "2022-12-04"}
    )
    circulation_list_2 = add_a_lot_of_elements(
        client, 10, {"borrowed_date": "2023-12-04"}
    )
    circulation_list_3 = add_a_lot_of_elements(
        client, 2, {"borrowed_date": "2022-01-04"}
    )
    circulation_list_4 = add_a_lot_of_elements(
        client, 5, {"borrowed_date": "2022-12-04"}
    )
    circulation_list_5 = add_a_lot_of_elements(
        client, 5, {"borrowed_date": "2022-12-10"}
    )
    circulation_list_6 = add_a_lot_of_elements(
        client, 2, {"borrowed_date": "2025-01-02"}
    )

    # Get all data with the filter

    current_circulation_list = get_all_circulations_filtered(
        client, "borrowed_date_start=2024-12-04"
    )
    print(f"current_circulation_list: {current_circulation_list}")
    expected_circulation_list = circulation_list_6
    assert len(current_circulation_list) == len(expected_circulation_list)
    assert current_circulation_list == expected_circulation_list

    current_circulation_list = get_all_circulations_filtered(
        client, "borrowed_date_end=2022-12-06"
    )
    expected_circulation_list = (
        circulation_list_1 + circulation_list_3 + circulation_list_4
    )
    assert len(current_circulation_list) == len(expected_circulation_list)
    assert current_circulation_list == expected_circulation_list

    current_circulation_list = get_all_circulations_filtered(
        client, "borrowed_date_start=2022-12-31&borrowed_date_end=2023-12-31"
    )
    expected_circulation_list = circulation_list_2
    assert len(current_circulation_list) == len(expected_circulation_list)
    assert current_circulation_list == expected_circulation_list

    current_circulation_list = get_all_circulations_filtered(
        client,
        f"borrowed_date_start={constants.DATE_DEFAULT_START_VALUE}&borrowed_date_end={constants.DATE_DEFAULT_END_VALUE}",
    )
    expected_circulation_list = (
        circulation_list_1
        + circulation_list_2
        + circulation_list_3
        + circulation_list_4
        + circulation_list_5
        + circulation_list_6
    )
    assert len(current_circulation_list) == len(expected_circulation_list)
    assert current_circulation_list == expected_circulation_list
