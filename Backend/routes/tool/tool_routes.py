from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from fastapi.params import Form, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Dict

from Backend.core.database import get_db
from Backend.crud.tool.crud_tool import tool_crud
from Backend.crud.user.crud_user import user_crud
from Backend.schemas.tool.tool_schema import ToolCreate, ToolResponse, ToolUpdate

router = APIRouter(
    prefix="/tools",
    tags=["tools"]
)

@router.post("/", response_model=ToolResponse)
async def create_tool(
    name: str = Form(...),
    description: str = Form(...),
    base_price: float = Form(...),
    tool_condition: str = Form(...),
    deposit: float = Form(...),
    current_user=Depends(user_crud.get_current_user),
    tool_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    raw_image_bytes = await tool_image.read()
    compressed_image_bytes = tool_crud.compress_image_bytes(raw_image_bytes)

    tool_data = ToolCreate(
        name=name,
        description=description,
        base_price=base_price,
        tool_condition=tool_condition,
        deposit=deposit,
        created_by=current_user.id,
        tool_image=compressed_image_bytes,
    )

    tool = tool_crud.create(db=db, obj_in=tool_data)

    return {
        "id": tool.id,
        "name": tool.name,
        "description": tool.description,
        "base_price": float(tool.base_price) if tool.base_price is not None else None,
        "deposit": float(tool.deposit) if tool.deposit is not None else None,
        "tool_condition": tool.tool_condition,
        "deleted": bool(tool.deleted),
        "deleted_at": tool.deleted_at,
        "creator_display_name": tool.creator.display_name if tool.creator else None,
        "creator_city": tool.creator.city if tool.creator else None,
        "creator_country": tool.creator.country if tool.creator else None,
    }

@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: int,
    name: str = Form(...),
    description: str = Form(...),
    base_price: float = Form(...),
    tool_condition: str = Form(...),
    deposit: float = Form(...),
    tool_image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    db_tool = tool_crud.get(db, tool_id)

    if not db_tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    update_data = {
        "name": name,
        "description": description,
        "base_price": base_price,
        "tool_condition": tool_condition,
        "deposit": deposit,
    }

    if tool_image is not None:
        image_bytes = await tool_image.read()
        update_data["tool_image"] = image_bytes

    tool = tool_crud.update(db, db_obj=db_tool, obj_in=ToolUpdate(**update_data, deleted=db_tool.deleted, deleted_at=db_tool.deleted_at))

    return {
        "id": tool.id,
        "name": tool.name,
        "description": tool.description,
        "base_price": float(tool.base_price) if tool.base_price is not None else None,
        "deposit": float(tool.deposit) if tool.deposit is not None else None,
        "tool_condition": tool.tool_condition,
        "deleted": bool(tool.deleted),
        "deleted_at": tool.deleted_at,
        "creator_display_name": tool.creator.display_name if tool.creator else None,
        "creator_city": tool.creator.city if tool.creator else None,
        "creator_country": tool.creator.country if tool.creator else None,
    }

@router.get("/", response_model=Dict)
def get_tools(
    name: str | None = Query(None),
    city: str | None = Query(None),
    zip: str | None = Query(None),
    country: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return tool_crud.get_filtered(db, name, city, zip, country, skip=skip, limit=limit)

@router.get("/user-tools", response_model=List[ToolResponse])
def get_tools(
    current_user=Depends(user_crud.get_current_user),
    db: Session = Depends(get_db)
):
    return tool_crud.get_user_tools(db, user_id=current_user.id)

@router.get("/image/{tool_id}")
def get_tool_image(tool_id: int, db: Session = Depends(get_db)):
    tool = tool_crud.get(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    if not tool.tool_image:
        raise HTTPException(
            status_code=404,
            detail="Tool image not found"
        )

    return Response(content=tool.tool_image, media_type="image/jpeg")

@router.get("/{tool_id}", response_model=ToolResponse)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = tool_crud.get(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    return tool


@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = tool_crud.delete(db, tool_id)

    if not tool:
        raise HTTPException(
            status_code=404,
            detail="Tool not found"
        )

    return {"message": "Tool deleted"}
