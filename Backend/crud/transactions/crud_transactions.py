from sqlalchemy.orm import Session
from Backend.crud.base import CRUDBase
from Backend.model.transactions.transactions_model import Transaction
from Backend.schemas.transactions.transaction_schema import TransactionCreate, TransactionUpdate


class CRUDTool(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_all_tools(self, db: Session, tool_id: int):
        query = db.query(Transaction).filter(Transaction.tool_id == tool_id).all()
        return query


transaction_crud = CRUDTool(Transaction)
