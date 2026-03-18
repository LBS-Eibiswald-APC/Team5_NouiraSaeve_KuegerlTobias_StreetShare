from sqlalchemy.orm import Session
from Backend.crud.base import CRUDBase
from Backend.model.request.requests import Requests
from Backend.model.tools.tools_model import Tool
from Backend.model.user.user_model import User
from Backend.schemas.requests.requests_schema import RequestsCreate, RequestsUpdate, RequestsResponse


class CRUDRequests(CRUDBase[Requests, RequestsCreate, RequestsUpdate]):
    def get_user_requests(self, current_user, db: Session):
        query = (
            db.query(
                Requests,
                Tool.name.label("name"),
                User.display_name.label("borrower_username")
            )
            .join(Tool, Requests.tool_id == Tool.id)
            .join(User, Requests.borrower_id == User.id)
            .filter(Requests.lender_id == current_user["id"])
            .all()
        )

        response = []
        for req, tool_name, borrower_username in query:
            response.append(
                RequestsResponse(
                    id=req.id,
                    tool_id=req.tool_id,
                    tool_name=tool_name,
                    to_respond_id=req.to_respond_it,
                    borrower_id=req.borrower_id,
                    borrower_username=borrower_username,
                    lender_id=req.lender_id,
                    start_date=req.start_date,
                    end_date=req.end_date,
                    created_at=req.created_at,
                    message=req.message,
                )
            )

        return response


requests_crud = CRUDRequests(Requests)
