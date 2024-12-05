import pytest
from fastapi.testclient import TestClient


def test_read_unknown_family(client: TestClient) -> None:
    response = client.get("/api/v1/families/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Family not found"


@pytest.mark.parametrize(
    "init_data",
    [
        {"email": "test_email"},
        {"phone_number": "phone_test"},
        {"email": "test_email", "phone_number": "phone_test"},
    ],
)
def test_read_created_family(client: TestClient, init_data: dict) -> None:
    response = client.post("/api/v1/families", json=init_data)
    assert response.status_code == 200
    created_data_response = response.json()

    response = client.get(f"/api/v1/families/{created_data_response["id"]}")
    assert response.status_code == 200

    data_response = response.json()
    for key, value in init_data.items():
        assert data_response[key] == value
    for key, value in created_data_response.items():
        assert data_response[key] == value


@pytest.mark.parametrize(
    "init_data",
    [
        {"email": "test_email"},
        {"phone_number": "phone_test"},
        {"email": "test_email", "phone_number": "phone_test"},
    ],
)
@pytest.mark.parametrize(
    "new_data",
    [
        {"email": "new_email"},
        {"phone_number": "new"},
        {"email": "new_test_email", "phone_number": "new_phone_test"},
        {},
    ],
)
def test_read_updated_family(
    client: TestClient, init_data: dict, new_data: dict
) -> None:
    response = client.post("/api/v1/families", json=init_data)
    assert response.status_code == 200
    created_data_response = response.json()

    response = client.patch(
        f"/api/v1/families/{created_data_response["id"]}", json=new_data
    )
    assert response.status_code == 200

    updated_data_expected = init_data
    for key, value in new_data.items():
        updated_data_expected[key] = value

    response = client.get(f"/api/v1/families/{created_data_response["id"]}")
    assert response.status_code == 200

    data_response = response.json()
    for key, value in init_data.items():
        assert data_response[key] == value
    for key, value in updated_data_expected.items():
        assert data_response[key] == value
