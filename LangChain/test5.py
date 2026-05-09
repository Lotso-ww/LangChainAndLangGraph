from typing import List, Tuple
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# 方法一
# def add(a:int, b:int) -> int:
#     """两数相加"""
#     return a + b
#
# add_tool = StructuredTool.from_function(add)

# 方法二
# class AddInput(BaseModel):
#     a: int = Field(..., description="第一个整数")
#     b: int = Field(..., description="第二个整数")
#
# def add(a:int, b:int) -> int:
#     return a + b
#
# add_tool = StructuredTool.from_function(
#     func=add,
#     name="add_tool",
#     description="两数相加",
#     args_schema=AddInput,
# )

# 方法三
class AddInput(BaseModel):
    a: int = Field(..., description="第一个整数")
    b: int = Field(..., description="第二个整数")

def add(a:int, b:int) -> Tuple[str, List[int]]:
    nums = [a,b]
    content = f"{nums}相加的结果是{a + b}"
    return content, nums

add_tool = StructuredTool.from_function(
    func=add,
    name="add_tool",       # 工具参数
    description="两数相加",  # 工具描述
    args_schema=AddInput,   # 工具参数
    response_format="content_and_artifact"
)

print(add_tool.invoke(
    {
        "name": "add_tool",
        "args": {"a": 3, "b": 4},
        "type": "tool_call", # 必填, invoke的类型
        "id": "1111" #必填,用来将工具调用请求和结果关联起来
    }
))
# print(add_tool.invoke({"a":2,"b":5}))
# print(add_tool.name)
# print(add_tool.description)
# print(add_tool.args)