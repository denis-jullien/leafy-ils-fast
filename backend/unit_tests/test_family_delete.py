from fastapi.testclient import TestClient


def test_delete_unknown_family(client: TestClient) -> None:
    response = client.delete("/api/v1/families/1")
    assert response.status_code == 404
    data_response = response.json()
    assert data_response["detail"] == "Family not found"


def test_delete_family(client: TestClient) -> None:
    data = {"email": "test_email", "phone_number": "phone_test"}
    response = client.post("/api/v1/families", json=data)
    assert response.status_code == 200
    data_response = response.json()

    response = client.delete(f"/api/v1/families/{data_response["id"]}")
    assert response.status_code == 204
    assert response.content == b""
