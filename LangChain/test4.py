from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing_extensions import Annotated

# 定义工具

# 方法一
# @tool
# def add(a: int, b: int) -> int:
#     """两数相加
#
#     Args:
#         a (int): a
#         b (int): b
#     """
#     return a + b

# # 方法二
# class AddInput(BaseModel):
#     """两数相加"""
#     a : int = Field(..., description="第一个整数")
#     b : int = Field(..., description="第二个整数")
#
# @tool(args_schema=AddInput)
# def add(a: int, b: int) -> int:
#     return a + b

# 方法三
@tool
def add(
        a: Annotated[int, ..., "第一个整数"],
        b: Annotated[int, ..., "第二个整数"]
) -> int:
    """两数相加

    Args:
        a (int): a
        b (int): b
    """
    return a + b
print(add.invoke({"a" : 2, "b" : 3}))
print(add.name)
print(add.description)
print(add.args)