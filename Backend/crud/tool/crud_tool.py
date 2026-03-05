from sqlalchemy.orm import Session, joinedload
from crud.base import CRUDBase
from model.tools.tools_model import Tool
from schemas.tool.tool_schema import ToolCreate, ToolUpdate

from Backend.model.user.user_model import User
from Backend.schemas.tool.tool_schema import ToolResponse


class CRUDTool(CRUDBase[Tool, ToolCreate, ToolUpdate]):
    def get_user_tools(
            self,
            db: Session,
            user_id: int
    ):
        query = (
            db.query(Tool)
            .join(User, Tool.created_by == User.id)
            .filter(User.id == user_id)
        ).all()
        response = []
        for t in query:
            response.append(ToolResponse(
                id=t.id,
                name=t.name,
                description=t.description,
                base_price=float(t.base_price) if t.base_price else None,
                deposit=float(t.deposit) if t.deposit else None,
                tool_condition=t.tool_condition,
                creator_display_name=t.creator.display_name if t.creator else None,
                creator_city=t.creator.city if t.creator else None,
                creator_country=t.creator.country if t.creator else None
            ))
        return response

    def get_filtered(
            self,
            db: Session,
            city: str | None = None,
            zip: str | None = None,
            country: str | None = None,
            skip = 0,
            limit = 25
    ):
        query = db.query(Tool).join(User)

        if city:
            query = query.filter(User.city.ilike(f"%{city}%"))
        if zip:
            query = query.filter(User.zip.ilike(f"%{zip}%"))
        if country:
            query = query.filter(User.country.ilike(f"%{country}%"))

        total = query.count()
        tools = query.offset(skip).limit(limit).options(joinedload(Tool.creator)).all()
        response = []
        for t in tools:
            response.append(ToolResponse(
                id=t.id,
                name=t.name,
                description=t.description,
                base_price=float(t.base_price) if t.base_price else None,
                deposit=float(t.deposit) if t.deposit else None,
                tool_condition=t.tool_condition,
                creator_display_name=t.creator.display_name if t.creator else None,
                creator_city=t.creator.city if t.creator else None,
                creator_country=t.creator.country if t.creator else None
            ))

        return {"tools": response, "total": total}

tool_crud = CRUDTool(Tool)
