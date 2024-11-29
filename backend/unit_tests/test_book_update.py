import pytest
import sys
from fastapi.testclient import TestClient

sys.path.append("backend")


def test_update_unknown_book(client: TestClient) -> None:
    new_data = {"author": "new_author"}

    response = client.patch("/books/1", json=new_data)
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
def test_update_book(client: TestClient, init_data: dict, new_data: dict) -> None:
    response = client.post("/books", json=init_data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.patch(f"/books/{data_response["id"]}", json=new_data)
    assert response.status_code == 200

    data_expected = init_data
    for key, value in new_data.items():
        if value is not None:
            data_expected[key] = value

    data_response = response.json()
    assert "id" in data_response
    for key, value in data_expected.items():
        assert data_response[key] == value
