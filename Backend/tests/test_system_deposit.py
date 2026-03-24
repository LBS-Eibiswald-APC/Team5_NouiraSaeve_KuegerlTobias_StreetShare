import pytest


def test_full_deposit_flow(client):

    lender_resp = client.post("/users/", json={
        "username": "lender_deposit",
        "email": "lender_deposit@example.com",
        "password": "securepass123",
        "city": "Teststadt",
    })
    assert lender_resp.status_code == 200
    lender = lender_resp.json()

    borrower_resp = client.post("/users/", json={
        "username": "borrower_deposit",
        "email": "borrower_deposit@example.com",
        "password": "securepass456",
        "city": "Teststadt",
    })
    assert borrower_resp.status_code == 200
    borrower = borrower_resp.json()

    tool_resp = client.post("/tools/", json={
        "name": "Schlagbohrer",
        "description": "Bohrer mit Kaution",
        "category": "Werkzeug",
        "city": "Teststadt",
        "owner_id": lender["id"],
        "deposit": 50.00,
    })
    assert tool_resp.status_code == 200
    tool = tool_resp.json()
    assert tool["deposit"] == 50.00

    transaction_resp = client.post("/transactions/", json={
        "tool_id": tool["id"],
        "borrower_id": borrower["id"],
        "lender_id": lender["id"],
        "start_date": "2025-03-01T09:00:00",
        "end_date": "2025-03-05T18:00:00",
    })
    assert transaction_resp.status_code == 200
    transaction = transaction_resp.json()
    assert "id" in transaction
    assert transaction["tool_id"] == tool["id"]

    get_resp = client.get(f"/transactions/{transaction['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["tool_id"] == tool["id"]
    assert fetched["borrower_id"] == borrower["id"]
    assert fetched["lender_id"] == lender["id"]

def test_deposit_tool_deleted(client, db_session):
    """TC-S-A-03: Deleting a tool sets tool_id to null in existing transactions (FK SET NULL)."""

    # --- Setup: Create lender user ---
    lender_resp = client.post("/users/", json={
        "username": "lender_del",
        "email": "lender_del@example.com",
        "password": "securepass123",
        "city": "Teststadt",
    })
    assert lender_resp.status_code == 200
    lender = lender_resp.json()

    borrower_resp = client.post("/users/", json={
        "username": "borrower_del",
        "email": "borrower_del@example.com",
        "password": "securepass456",
        "city": "Teststadt",
    })
    assert borrower_resp.status_code == 200
    borrower = borrower_resp.json()

    tool_resp = client.post("/tools/", json={
        "name": "Stichsäge",
        "description": "Säge mit Kaution",
        "category": "Werkzeug",
        "city": "Teststadt",
        "owner_id": lender["id"],
        "deposit": 50.00,
    })
    assert tool_resp.status_code == 200
    tool = tool_resp.json()

    transaction_resp = client.post("/transactions/", json={
        "tool_id": tool["id"],
        "borrower_id": borrower["id"],
        "lender_id": lender["id"],
        "start_date": "2025-04-01T09:00:00",
        "end_date": "2025-04-05T18:00:00",
    })
    assert transaction_resp.status_code == 200
    transaction = transaction_resp.json()
    assert transaction["tool_id"] == tool["id"]

    delete_resp = client.delete(f"/tools/{tool['id']}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/transactions/{transaction['id']}")
    assert get_resp.status_code == 200
    fetched = get_resp.json()
    assert fetched["tool_id"] is None
    assert fetched["borrower_id"] == borrower["id"]
    assert fetched["lender_id"] == lender["id"]

