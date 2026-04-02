from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from Backend.crud.base import CRUDBase
from Backend.model.request.requests import Requests
from Backend.model.tools.tools_model import Tool
from Backend.model.user.user_model import User
from Backend.model.transactions.transactions_model import Transaction
from Backend.schemas.requests.requests_schema import RequestsCreate, RequestsUpdate, RequestsResponse


class CRUDRequests(CRUDBase[Requests, RequestsCreate, RequestsUpdate]):
    def check_if_requested_already(self, tool_id: int, borrower_id: int, db: Session):
        return db.query(Requests).filter(
            Requests.tool_id == tool_id,
            Requests.borrower_id == borrower_id,
            Requests.status == "Ausstehend"
        ).all()

    def check_if_rejected_before(self, tool_id: int, borrower_id: int, db: Session):
        return db.query(Requests).filter(
            Requests.tool_id == tool_id,
            Requests.borrower_id == borrower_id,
            Requests.status == "Abgelehnt"
        ).first()

    def get_latest_for_conversation(self, db: Session, conversation):
        if conversation is None:
            return None

        user_ids = [conversation.user1_id, conversation.user2_id]

        return (
            db.query(Requests)
            .filter(
                or_(
                    Requests.tool_id == conversation.tool_id,
                    and_(
                        Requests.borrower_id.in_(user_ids),
                        Requests.lender_id.in_(user_ids),
                    ),
                ),
            )
            .order_by(Requests.created_at.desc(), Requests.id.desc())
            .first()
        )

    def is_conversation_rejected(self, db: Session, conversation) -> bool:
        latest_request = self.get_latest_for_conversation(db, conversation)
        return latest_request is not None and latest_request.status == "Abgelehnt"

    def _apply_request_filters(self, query, search: str | None = None, status: str | None = None):
        if search and search.strip():
            search_value = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Tool.name.ilike(search_value),
                    User.display_name.ilike(search_value),
                    Requests.message.ilike(search_value),
                )
            )

        if status:
            query = query.filter(Requests.status == status)

        return query

    def _build_request_response(self, rows):
        response = []
        for req, tool_name, tool_deposit, borrower_username, transaction_id in rows:
            response.append(
                RequestsResponse(
                    id=req.id,
                    tool_id=req.tool_id,
                    tool_name=tool_name,
                    tool_deposit=float(tool_deposit) if tool_deposit is not None else None,
                    to_respond_id=req.to_respond_id,
                    borrower_id=req.borrower_id,
                    borrower_username=borrower_username,
                    lender_id=req.lender_id,
                    start_date=req.start_date,
                    end_date=req.end_date,
                    created_at=req.created_at,
                    message=req.message,
                    status=req.status,
                    has_transaction=transaction_id is not None,
                    transaction_id=transaction_id,
                )
            )

        return response

    def get_user_requests(self, current_user, db: Session, search: str | None = None, status: str | None = None, skip: int = 0, limit: int = 10):
        query = (
            db.query(
                Requests,
                Tool.name.label("name"),
                Tool.deposit.label("tool_deposit"),
                User.display_name.label("borrower_username"),
                Transaction.id.label("transaction_id"),
            )
            .join(Tool, Requests.tool_id == Tool.id)
            .join(User, Requests.borrower_id == User.id)
            .outerjoin(Transaction, Transaction.request_id == Requests.id)
            .filter(Requests.lender_id == current_user.id)
        )

        query = self._apply_request_filters(query, search=search, status=status)
        total = query.count()
        rows = query.order_by(Requests.created_at.desc()).offset(skip).limit(limit).all()

        return {"requests": self._build_request_response(rows), "total": total}

    def get_sending_user_requests(self, current_user, db: Session, search: str | None = None, status: str | None = None, skip: int = 0, limit: int = 10):
        query = (
            db.query(
                Requests,
                Tool.name.label("name"),
                Tool.deposit.label("tool_deposit"),
                User.display_name.label("borrower_username"),
                Transaction.id.label("transaction_id"),
            )
            .join(Tool, Requests.tool_id == Tool.id)
            .join(User, Requests.lender_id == User.id)
            .outerjoin(Transaction, Transaction.request_id == Requests.id)
            .filter(Requests.borrower_id == current_user.id)
        )

        query = self._apply_request_filters(query, search=search, status=status)
        total = query.count()
        rows = query.order_by(Requests.created_at.desc()).offset(skip).limit(limit).all()

        return {"requests": self._build_request_response(rows), "total": total}

    def get_all_tools(self, db: Session, tool_id: int):
        query = (
            db.query(
                Requests,
                Tool.name.label("name"),
                Tool.deposit.label("tool_deposit"),
                User.display_name.label("borrower_username"),
                Transaction.id.label("transaction_id"),
            )
            .join(Tool, Requests.tool_id == Tool.id)
            .join(User, Requests.borrower_id == User.id)
            .outerjoin(Transaction, Transaction.request_id == Requests.id)
            .filter(Requests.tool_id == tool_id)
            .all()
        )

        return self._build_request_response(query)


requests_crud = CRUDRequests(Requests)
