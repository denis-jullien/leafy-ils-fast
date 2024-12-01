from fastapi.testclient import TestClient


def test_delete_unknown_book(client: TestClient) -> None:
    response = client.delete("/api/v1/books/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Book not found"


def test_delete_book(client: TestClient) -> None:
    data = {
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
    response = client.post("/api/v1/books", json=data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.delete(f"/api/v1/books/{data_response["id"]}")
    assert response.status_code == 200
