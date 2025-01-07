import pytest
from fastapi.testclient import TestClient


def test_update_unknown_family(client: TestClient) -> None:
    new_data = {"email": "new_test_email", "phone_number": "new_phone_test"}

    response = client.patch("/api/v1/families/1", json=new_data)
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Family not found"


@pytest.mark.parametrize(
    "init_data",
    [
        {"email": "test_email"},
        {"phone_number": "phone_test"},
        {
            "email": "test_email",
            "phone_number": "phone_test",
            "last_adhesion_date": "2025-01-06",
        },
    ],
)
@pytest.mark.parametrize(
    "new_data",
    [
        {"email": "new_email"},
        {"phone_number": "new"},
        {"last_adhesion_date": "2024-12-06"},
        {
            "email": "new_test_email",
            "phone_number": "new_phone_test",
            "last_adhesion_date": "2022-01-06",
        },
        {},
    ],
)
def test_update_family(client: TestClient, init_data: dict, new_data: dict) -> None:
    response = client.post("/api/v1/families", json=init_data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.patch(f"/api/v1/families/{data_response["id"]}", json=new_data)
    assert response.status_code == 200

    data_expected = init_data
    for key, value in new_data.items():
        data_expected[key] = value

    data_response = response.json()
    assert "id" in data_response
    for key, value in data_expected.items():
        assert data_response[key] == value
