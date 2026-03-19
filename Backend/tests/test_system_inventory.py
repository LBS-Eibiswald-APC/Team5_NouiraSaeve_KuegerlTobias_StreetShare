import pytest

def test_inventory_filter_flow(client):

    tool_data = {
        "name": "TestTool",
        "description": "A tool for testing inventory filter flow.",
        "city": "Teststadt"
    }

    create_response = client.post("/tools/", json=tool_data)
    assert create_response.status_code == 200 or create_response.status_code == 201
    created_tool = create_response.json()
    tool_id = created_tool["id"]

    list_response = client.get("/tools/", params={"city": "Teststadt"})
    assert list_response.status_code == 200
    list_data = list_response.json()
    assert list_data["total"] >= 1

    detail_response = client.get(f"/tools/{tool_id}")
    assert detail_response.status_code == 200
    detail_data = detail_response.json()
    assert detail_data["name"] == "TestTool"
    assert detail_data["description"] == "A tool for testing inventory filter flow."
    assert detail_data["city"] == "Teststadt"
