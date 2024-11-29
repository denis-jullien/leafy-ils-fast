import pytest
import sys
from fastapi.testclient import TestClient

sys.path.append("backend")


@pytest.mark.parametrize(
    "data",
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
def test_create_book(client: TestClient, data: dict) -> None:
    response = client.post("/books", json=data)
    assert response.status_code == 200

    data_response = response.json()
    assert "id" in data_response
    for key, value in data.items():
        assert data_response[key] == value
