import pytest
from fastapi.testclient import TestClient


def test_update_unknown_book(client: TestClient) -> None:
    new_data = {"author": "new_author"}

    response = client.patch("/api/v1/books/1", json=new_data)
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
            "abstract": "new_abstract",
            "publisher": "new_publisher",
            "catalog": "new_catalog",
            "category_type": "new_category_type",
            "category_age": "new_category_age",
            "category_topics": "new_category_topics",
            "language": "en",
            "cover": "new_cover",
            "available": True,
            "archived": False,
        },
        {},
    ],
)
def test_update_book(client: TestClient, init_data: dict, new_data: dict) -> None:
    response = client.post("/api/v1/books", json=init_data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.patch(f"/api/v1/books/{data_response["id"]}", json=new_data)
    assert response.status_code == 200

    data_expected = init_data
    for key, value in new_data.items():
        if value is not None:
            data_expected[key] = value

    data_response = response.json()
    assert "id" in data_response
    for key, value in data_expected.items():
        assert data_response[key] == value
