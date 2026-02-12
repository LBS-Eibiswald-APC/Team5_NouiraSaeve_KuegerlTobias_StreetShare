from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Backend.core.database import get_db
from Backend.crud.transactions.crud_transactions import transaction_crud
from Backend.model.transactions.transactions_model import Transaction
from Backend.schemas.transactions.transaction_schema import TransactionCreate, TransactionUpdate, TransactionResponse


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return transaction_crud.create(db, transaction)


@router.get("/", response_model=List[TransactionResponse])
def get_tools(db: Session = Depends(get_db)):
    return transaction_crud.get_all(db)


@router.get("/{tool_id}", response_model=TransactionResponse)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = transaction_crud.get(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    return tool


@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = transaction_crud.delete(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    return {"message": "Tool deleted"}
