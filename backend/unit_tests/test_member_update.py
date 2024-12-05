import pytest
from fastapi.testclient import TestClient


def test_update_unknown_member(client: TestClient) -> None:
    new_data = {
        "firstname": "firstname",
        "surname": "surname",
        "family_referent": True,
        "birthdate": "2019-12-04",
        "family_id": 1,
    }

    response = client.patch("/api/v1/members/1", json=new_data)
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Member not found"


@pytest.mark.parametrize(
    "init_data",
    [
        {"firstname": "firstname", "surname": "surname"},
        {
            "firstname": "firstname",
            "surname": "surname",
            "family_referent": True,
            "birthdate": "2019-12-04",
            "family_id": 1,
        },
    ],
)
@pytest.mark.parametrize(
    "new_data",
    [
        {"firstname": "firstname"},
        {"surname": "update"},
        {"family_referent": False},
        {"birthdate": "2020-12-04"},
        {"family_id": 2},
        {
            "firstname": "Prenom",
            "surname": "update",
            "family_referent": False,
            "birthdate": "2020-12-04",
            "family_id": 2,
        },
        {},
    ],
)
def test_update_member(client: TestClient, init_data: dict, new_data: dict) -> None:
    # add family 1
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200
    # add family 2
    family_data = {"email": "test_email2", "phone_number": "phone_test2"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200
    # add member
    response = client.post("/api/v1/members", json=init_data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.patch(f"/api/v1/members/{data_response["id"]}", json=new_data)
    assert response.status_code == 200

    data_expected = init_data
    for key, value in new_data.items():
        data_expected[key] = value

    data_response = response.json()
    assert "id" in data_response
    for key, value in data_expected.items():
        assert data_response[key] == value
