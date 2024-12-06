import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "data",
    [
        {"firstname": "firstname", "surname": "surname"},
        {"firstname": "firstname", "surname": "surname", "family_referent": True},
        {"firstname": "firstname", "surname": "surname", "birthdate": "2019-12-04"},
        {"firstname": "firstname", "surname": "surname", "family_id": 1},
        {
            "firstname": "firstname",
            "surname": "surname",
            "family_referent": True,
            "birthdate": "2019-12-04",
            "family_id": 1,
        },
    ],
)
def test_create_member(client: TestClient, data: dict) -> None:
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200

    response = client.post("/api/v1/members", json=data)
    assert response.status_code == 200

    data_response = response.json()
    if "family_referent" not in data:
        data["family_referent"] = False
    assert "id" in data_response
    for key, value in data.items():
        assert data_response[key] == value
