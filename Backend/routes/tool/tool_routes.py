from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from crud.tool.crud_tool import tool_crud
from schemas.tool.tool_schema import ToolCreate, ToolResponse


router = APIRouter(
    prefix="/tools",
    tags=["tools"]
)


@router.post("/", response_model=ToolResponse)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    return tool_crud.create(db, tool)


@router.get("/", response_model=List[ToolResponse])
def get_tools(db: Session = Depends(get_db)):
    return tool_crud.get_all(db)


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
