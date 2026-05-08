from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# 方法一
# def add(a:int, b:int) -> int:
#     """两数相加"""
#     return a + b
#
# add_tool = StructuredTool.from_function(add)

# 方法二
class AddInput(BaseModel):
    a: int = Field(..., description="第一个整数")
    b: int = Field(..., description="第二个整数")

def add(a:int, b:int) -> int:
    return a + b

add_tool = StructuredTool.from_function(
    func=add,
    name="add_tool",
    description="两数相加",
    args_schema=AddInput,
)
print(add_tool.invoke({"a":2,"b":5}))
print(add_tool.name)
print(add_tool.description)
print(add_tool.args)