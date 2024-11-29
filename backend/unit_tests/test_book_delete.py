import sys
from fastapi.testclient import TestClient

sys.path.append("backend")
from tools import *


def test_delete_unknown_book(client: TestClient) -> None:
    response = client.delete("/books/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Book not found"


def test_delete_book(client: TestClient) -> None:
    data = {
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
    }
    response = client.post("/books", json=data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.delete(f"/books/{data_response["id"]}")
    assert response.status_code == 200
