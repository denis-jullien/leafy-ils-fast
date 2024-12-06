import pytest
from fastapi.testclient import TestClient


def test_read_unknown_member(client: TestClient) -> None:
    response = client.get("/api/v1/members/1")
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
def test_read_created_member(client: TestClient, init_data: dict) -> None:
    response = client.post("/api/v1/members", json=init_data)
    assert response.status_code == 200
    created_data_response = response.json()

    response = client.get(f"/api/v1/members/{created_data_response["id"]}")
    assert response.status_code == 200

    data_response = response.json()
    for key, value in init_data.items():
        assert data_response[key] == value
    for key, value in created_data_response.items():
        assert data_response[key] == value


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
def test_read_updated_member(
    client: TestClient, init_data: dict, new_data: dict
) -> None:
    response = client.post("/api/v1/members", json=init_data)
    assert response.status_code == 200
    created_data_response = response.json()

    response = client.patch(
        f"/api/v1/members/{created_data_response["id"]}", json=new_data
    )
    assert response.status_code == 200

    updated_data_expected = init_data
    for key, value in new_data.items():
        updated_data_expected[key] = value

    response = client.get(f"/api/v1/members/{created_data_response["id"]}")
    assert response.status_code == 200

    data_response = response.json()
    for key, value in init_data.items():
        assert data_response[key] == value
    for key, value in updated_data_expected.items():
        assert data_response[key] == value
