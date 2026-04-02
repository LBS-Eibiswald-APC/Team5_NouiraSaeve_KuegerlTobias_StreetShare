from sqlalchemy.orm import Session, aliased

from Backend.crud.base import CRUDBase
from Backend.model.tools.tools_model import Tool
from Backend.model.transaction_reviews.transaction_reviews_model import TransactionReview
from Backend.model.transactions.transactions_model import Transaction
from Backend.model.user.user_model import User
from Backend.schemas.transaction_reviews.transaction_reviews_schema import (
    TransactionReviewCreate,
    TransactionReviewUpdate,
)


class CRUDTransactionReviews(CRUDBase[TransactionReview, TransactionReviewCreate, TransactionReviewUpdate]):
    def get_by_transaction_id(self, db: Session, transaction_id: int):
        return db.query(TransactionReview).filter(TransactionReview.transaction_id == transaction_id).first()

    def get_all_with_details(self, db: Session):
        borrower = aliased(User)
        lender = aliased(User)

        return (
            db.query(
                TransactionReview,
                Transaction,
                Tool.name.label("tool_name"),
                borrower.display_name.label("borrower_name"),
                lender.display_name.label("lender_name"),
            )
            .join(Transaction, TransactionReview.transaction_id == Transaction.id)
            .join(Tool, Transaction.tool_id == Tool.id)
            .outerjoin(borrower, TransactionReview.borrower_id == borrower.id)
            .outerjoin(lender, TransactionReview.lender_id == lender.id)
            .order_by(TransactionReview.created_at.desc())
            .all()
        )

    def build_review_response(self, rows):
        response = []

        for review, transaction, tool_name, borrower_name, lender_name in rows:
            response.append({
                "id": review.id,
                "transaction_id": review.transaction_id,
                "tool_id": transaction.tool_id if transaction else None,
                "tool_name": tool_name,
                "borrower_id": review.borrower_id,
                "borrower_name": borrower_name,
                "lender_id": review.lender_id,
                "lender_name": lender_name,
                "borrower_condition": review.borrower_condition,
                "lender_condition": review.lender_condition,
                "has_lender_picture": review.lender_picture is not None,
                "review_status": review.review_status,
                "support_decision_condition": review.support_decision_condition,
                "support_note": review.support_note,
                "created_at": review.created_at,
                "resolved_at": review.resolved_at,
                "resolved_by": review.resolved_by,
                "transaction_status": transaction.status if transaction else None,
                "final_condition": transaction.final_condition if transaction else None,
            })

        return response


transaction_review_crud = CRUDTransactionReviews(TransactionReview)
