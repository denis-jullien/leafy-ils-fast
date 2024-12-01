import pytest
import sys
from fastapi.testclient import TestClient

from .tools import *


@pytest.mark.parametrize(
    "data",
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
def test_create_book(client: TestClient, data: dict) -> None:
    response = client.post("/api/v1/books", json=data)
    assert response.status_code == 200

    data_response = response.json()
    assert "id" in data_response
    for key, value in data.items():
        assert data_response[key] == value
