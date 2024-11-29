import pytest
import sys
from fastapi.testclient import TestClient

sys.path.append("backend")


def test_read_unknown_book(client: TestClient) -> None:
    response = client.get("/books/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Book not found"


@pytest.mark.parametrize(
    "init_data",
    [
        {"title": "title", "author": "author"},
        {
            "title": "title",
            "author": "author",
            "synopsis": "synopsis",
            "edition": "edition",
            "catalog": "catalog",
            "category_type": "category_type",
            "category_age": "category_age",
            "category_topics": "category_topics",
            "langage": "langage",
            "cover": "cover",
            "available": False,
            "archived": True,
        },
    ],
)
def test_read_created_book(client: TestClient, init_data: dict) -> None:
    response = client.post("/books", json=init_data)
    assert response.status_code == 200
    created_data_response = response.json()

    response = client.get(f"/books/{created_data_response["id"]}")
    assert response.status_code == 200

    data_response = response.json()
    for key, value in init_data.items():
        assert data_response[key] == value
    for key, value in created_data_response.items():
        assert data_response[key] == value


@pytest.mark.parametrize(
    "init_data",
    [
        {"title": "title", "author": "author"},
        {
            "title": "title",
            "author": "author",
            "synopsis": "synopsis",
            "edition": "edition",
            "catalog": "catalog",
            "category_type": "category_type",
            "category_age": "category_age",
            "category_topics": "category_topics",
            "langage": "langage",
            "cover": "cover",
            "available": False,
            "archived": True,
        },
    ],
)
@pytest.mark.parametrize(
    "new_data",
    [
        {"author": "new_author"},
        {
            "title": "new_title",
            "author": "new_author",
            "synopsis": "new_synopsis",
            "edition": "new_edition",
            "catalog": "new_catalog",
            "category_type": "new_category_type",
            "category_age": "new_category_age",
            "category_topics": "new_category_topics",
            "langage": "new_langage",
            "cover": "new_cover",
            "available": True,
            "archived": False,
        },
        {},
    ],
)
def test_read_updated_book(client: TestClient, init_data: dict, new_data: dict) -> None:
    response = client.post("/books", json=init_data)
    assert response.status_code == 200
    created_data_response = response.json()

    response = client.patch(f"/books/{created_data_response["id"]}", json=new_data)
    assert response.status_code == 200

    updated_data_expected = init_data
    for key, value in new_data.items():
        if value is not None:
            updated_data_expected[key] = value

    response = client.get(f"/books/{created_data_response["id"]}")
    assert response.status_code == 200

    data_response = response.json()
    for key, value in init_data.items():
        assert data_response[key] == value
    for key, value in updated_data_expected.items():
        assert data_response[key] == value
