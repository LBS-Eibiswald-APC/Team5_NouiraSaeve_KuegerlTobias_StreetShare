from sqlalchemy.orm import Session
from crud.base import CRUDBase
from model.tools.tools_model import Tool
from schemas.tool.tool_schema import ToolCreate, ToolUpdate


class CRUDTool(CRUDBase[Tool, ToolCreate, ToolUpdate]):
    pass


tool_crud = CRUDTool(Tool)
