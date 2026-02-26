from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from Backend.core.database import get_db
from Backend.crud.tool.crud_tool import tool_crud
from Backend.schemas.tool.tool_schema import ToolCreate, ToolResponse


router = APIRouter(
    prefix="/tools",
    tags=["tools"]
)


@router.post("/", response_model=ToolResponse)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    return tool_crud.create(db, tool)


@router.get("/", response_model=List[ToolResponse])

def get_tools(
    city: str | None = Query(None),
    zip: str | None = Query(None),
    country: str | None = Query(None),
    db: Session = Depends(get_db)
):
    return tool_crud.get_filtered(db, city, zip, country)


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
