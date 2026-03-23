from sqlalchemy.orm import Session, joinedload
from Backend.crud.base import CRUDBase
from Backend.model.tools.tools_model import Tool
from Backend.schemas.tool.tool_schema import ToolCreate, ToolUpdate

from Backend.model.user.user_model import User
from Backend.schemas.tool.tool_schema import ToolResponse

from io import BytesIO
from PIL import Image, ImageOps



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
                creator_country=t.creator.country if t.creator else None,
                deleted=t.deleted,
                deleted_at=t.deleted_at
            ))
        return response

    def compress_image_bytes(self, image_bytes: bytes, max_size=(1600, 1600), quality=82) -> bytes:
        input_buffer = BytesIO(image_bytes)

        with Image.open(input_buffer) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGB")
            img.thumbnail(max_size)

            output_buffer = BytesIO()
            img.save(output_buffer, format="JPEG", quality=quality, optimize=True)

            return output_buffer.getvalue()

    def get_filtered(
            self,
            db: Session,
            name: str | None = None,
            city: str | None = None,
            zip: str | None = None,
            country: str | None = None,
            skip=0,
            limit=25
    ):
        query = db.query(Tool).join(User)

        if name:
            query = query.filter(Tool.name.ilike(f"%{name}%"))
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
                creator_country=t.creator.country if t.creator else None,
                deleted=t.deleted,
                deleted_at=t.deleted_at
            ))

        return {"tools": response, "total": total}

tool_crud = CRUDTool(Tool)
