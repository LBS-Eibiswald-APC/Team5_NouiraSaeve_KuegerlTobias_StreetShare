import pytest

def test_create_tool(client):
    response = client.post("/tools/", json={
        "name": "Hammer",
        "description": "A useful tool for hitting nails."
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Hammer"
    assert data["description"] == "A useful tool for hitting nails."
    assert "id" in data

def test_get_tool_by_id(client):
    response = client.get("/tools/1")

    assert response.status_code == 200
    assert response.json["tool"]["id"] is not None
    assert response.json["tool"]["name"] is not None
    assert response.json["tool"]["description"] is not None