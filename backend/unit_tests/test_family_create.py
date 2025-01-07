import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "data",
    [
        {"email": "test_email", "phone_number": "phone_test"},
        {
            "email": "test@a.a",
            "phone_number": "003254",
            "last_adhesion_date": "2025-01-07",
        },
        {"email": "test_email"},
        {"phone_number": "phone_test"},
    ],
)
def test_create_family_with_success(client: TestClient, data: dict) -> None:
    response = client.post("/api/v1/families", json=data)
    assert response.status_code == 200

    data_response = response.json()
    assert "id" in data_response
    for key, value in data.items():
        assert data_response[key] == value


@pytest.mark.parametrize(
    "data",
    [{}, {"last_adhesion_date": "2025-01-07"}],
)
def test_create_family_with_failure(client: TestClient, data: dict) -> None:
    response = client.post("/api/v1/families", json=data)
    assert response.status_code == 422
    data_response = response.json()
    assert "detail" in data_response
