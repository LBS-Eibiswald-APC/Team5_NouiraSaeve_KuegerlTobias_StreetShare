import pytest
from pydantic import ValidationError
from Backend.schemas.tool.tool_schema import ToolCreate


def test_tool_create_valid():
    tool = ToolCreate(
        name="Hammer",
        description="test_tool_schema.py::test_tool_create_valid"
    )
    assert tool.name == "Hammer"
    assert tool.description == "test_tool_schema.py::test_tool_create_valid"
    assert tool.base_price is None
    assert tool.deposit is None
    assert tool.tool_condition is None
    assert tool.created_by is None

def test_tool_create_missing_name():
    with pytest.raises(ValidationError):
        ToolCreate(
            description="test_tool_schema.py::test_tool_create_missing_name"
        )


