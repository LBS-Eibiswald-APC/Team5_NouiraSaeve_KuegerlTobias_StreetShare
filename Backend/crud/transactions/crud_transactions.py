from sqlalchemy.orm import Session
from Backend.crud.base import CRUDBase
from Backend.model.transactions.transactions_model import Transaction
from Backend.schemas.transactions.transaction_schema import TransactionCreate, TransactionUpdate


class CRUDTool(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    pass


transaction_crud = CRUDTool(Transaction)
