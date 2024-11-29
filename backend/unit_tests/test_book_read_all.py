import sys
from fastapi.testclient import TestClient

sys.path.append("backend")


def test_read_all_book_without_book(client: TestClient) -> None:
    response = client.get("/books")
    assert response.status_code == 200
    data_response = response.json()
    assert data_response == []


def test_read_all_book_with_pagination(client: TestClient) -> None:
    book_list = list()
    init_data = {
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
    for _ in range(150):
        response = client.post("/books", json=init_data)
        assert response.status_code == 200
        book_list.append(response.json())

    # Get All books with offset default: 0 and limit default: 100
    response = client.get("/books")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 100
    for book in book_list[0:100]:
        assert book in data_response

    # Get All books with offset: 110 and limit: 10
    response = client.get("/books?offset=110&limit=10")
    assert response.status_code == 200
    data_response = response.json()
    assert len(data_response) == 10
    for book in book_list[110:120]:
        assert book in data_response
