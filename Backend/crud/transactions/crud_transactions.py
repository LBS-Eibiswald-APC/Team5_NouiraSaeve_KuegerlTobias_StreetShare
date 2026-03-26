from sqlalchemy.orm import Session, aliased
from Backend.crud.base import CRUDBase
from Backend.model.transactions.transactions_model import Transaction
from Backend.model.tools.tools_model import Tool
from Backend.model.user.user_model import User
from Backend.schemas.transactions.transaction_schema import TransactionCreate, TransactionUpdate


class CRUDTool(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_by_request_id(self, db: Session, request_id: int):
        return db.query(Transaction).filter(Transaction.request_id == request_id).first()

    def _build_transaction_response(self, rows):
        response = []

        for transaction, tool_name, borrower_name, lender_name in rows:
            response.append({
                "id": transaction.id,
                "tool_id": transaction.tool_id,
                "request_id": transaction.request_id,
                "tool_name": tool_name,
                "borrower_id": transaction.borrower_id,
                "borrower_name": borrower_name,
                "lender_id": transaction.lender_id,
                "lender_name": lender_name,
                "start_date": transaction.start_date,
                "end_date": transaction.end_date,
                "created_at": transaction.created_at,
                "picture_before": transaction.picture_before,
                "picture_after": transaction.picture_after,
            })

        return response

    def get_all_tools(self, db: Session, tool_id: int):
        borrower = aliased(User)
        lender = aliased(User)

        query = (
            db.query(
                Transaction,
                Tool.name.label("tool_name"),
                borrower.display_name.label("borrower_name"),
                lender.display_name.label("lender_name"),
            )
            .join(Tool, Transaction.tool_id == Tool.id)
            .join(borrower, Transaction.borrower_id == borrower.id)
            .join(lender, Transaction.lender_id == lender.id)
            .filter(Transaction.tool_id == tool_id)
            .all()
        )
        return self._build_transaction_response(query)

    def get_user_transactions(self, db: Session, current_user_id: int):
        borrower = db.query(User).subquery()
        lender = db.query(User).subquery()

        query = (
            db.query(
                Transaction,
                Tool.name.label("tool_name"),
                borrower.c.display_name.label("borrower_name"),
                lender.c.display_name.label("lender_name"),
            )
            .join(Tool, Transaction.tool_id == Tool.id)
            .join(borrower, Transaction.borrower_id == borrower.c.id)
            .join(lender, Transaction.lender_id == lender.c.id)
            .filter(
                (Transaction.borrower_id == current_user_id) |
                (Transaction.lender_id == current_user_id)
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

        return self._build_transaction_response(query)


transaction_crud = CRUDTool(Transaction)
