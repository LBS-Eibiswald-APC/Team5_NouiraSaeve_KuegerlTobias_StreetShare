import pytest
from datetime import datetime

def test_create_transaction(client, db_session):

    lender_response = client.post("/users/", json={
        "username": "lender_user",
        "email": "lender@example.com",
        "password": "securepass123",
        "city": "Teststadt"
    })

    assert lender_response.status_code == 200
    lender = lender_response.json()

    borrower_response = client.post("/users/", json={
        "username": "borrower_user",
        "email": "borrower@example.com",
        "password": "securepass456",
        "city": "Teststadt",
    })

    assert borrower_response.status_code == 200
    borrower = borrower_response.json()

    tool_response = client.post("/tools/", json={
        "name": "Bohrmaschine",
        "description": "Eine Testbohrmaschine",
        "category": "Werkzeug",
        "city": "Teststadt",
        "owner_id": lender["id"],
    })
    assert tool_response.status_code == 200
    tool = tool_response.json()

    transaction_data = {
        "tool_id": tool["id"],
        "borrower_id": borrower["id"],
        "lender_id": lender["id"],
        "start_date": "2025-02-01T10:00:00",
        "end_date": "2025-02-05T18:00:00",
    }
    response = client.post("/transactions/", json=transaction_data)

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["tool_id"] == tool["id"]
    assert data["borrower_id"] == borrower["id"]
    assert data["lender_id"] == lender["id"]
    assert data["start_date"] is not None
    assert data["end_date"] is not None