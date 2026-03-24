import pytest
from datetime import datetime
from Backend.schemas.transactions.transaction_schema import TransactionCreate

def test_transaction_create_valid():
    data = {
        "tool_id": 1,
        "borrower_id": 2,
        "lender_id": 3,
        "start_date": "2025-01-15T10:00:00",
        "end_date": "2025-01-20T10:00:00",
    }

    transaction = TransactionCreate(**data)

    assert transaction.tool_id == 1
    assert transaction.borrower_id == 2
    assert transaction.lender_id == 3

    assert isinstance(transaction.start_date, datetime)
    assert isinstance(transaction.end_date, datetime)