from fastapi.testclient import TestClient


def test_delete_unknown_member(client: TestClient) -> None:
    response = client.delete("/api/v1/members/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Member not found"


def test_delete_member(client: TestClient) -> None:
    family_data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=family_data)
    assert response.status_code == 200

    data = {
        "firstname": "firstname",
        "surname": "surname",
        "family_referent": True,
        "birthdate": "2019-12-04",
        "family_id": 1,
    }
    response = client.post("/api/v1/members", json=data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.delete(f"/api/v1/members/{data_response["id"]}")
    assert response.status_code == 204
    assert response.content == b""
