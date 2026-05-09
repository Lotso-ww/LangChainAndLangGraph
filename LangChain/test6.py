from langchain_core.messages import HumanMessage
from langchain_deepseek import ChatDeepSeek
from typing_extensions import Annotated
from langchain_core.tools import tool


@tool
def add(
        a: Annotated[int, ..., "第一个参数"],
        b: Annotated[int, ..., "第二个参数"]
) -> int:
    """两数相加"""
    return a + b

@tool
def multiply(
        a: Annotated[int, ..., "第一个参数"],
        b: Annotated[int, ..., "第二个参数"]
) -> int:
    """两数相乘"""
    return a * b

model = ChatDeepSeek(model="deepseek-v4-flash")

# 绑定工具
tools = [add, multiply]
model_with_tool = model.bind_tools(tools=tools)
# 强制调用 -- 不过这个地方deepseek好像是不太支持的，gpt是可以的
# model_with_tool = model.bind_tools(tools=tools, tool_choice="any")


# 调用工具
# print(model_with_tool.invoke("2乘3等于多少?"))
# print(model_with_tool.invoke("你是谁?"))

# ai_msg = model_with_tool.invoke("2乘3等于多少?")
# tool_result = multiply.invoke(ai_msg.tool_calls[0])
# print(tool_result)

# 定义消息列表: 添加要传递给聊天模型的消息
message = [
    HumanMessage("2乘3等于多少? 6加6等于多少?")
]
ai_msg = model_with_tool.invoke(message)
# print(ai_msg)
# tool_calls=[
# {'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'call_00_wWnKUSl9hlBWOMJFXdsd8704', 'type': 'tool_call'},
# {'name': 'add', 'args': {'a': 6, 'b': 6}, 'id': 'call_01_f6F4dM9i6L19Ny98gtzy1183', 'type': 'tool_call'}
# ]
message.append(ai_msg)

# 构建ToolMessage, 并且添加到消息列表中
for tool_call in ai_msg.tool_calls:
    selected_tools = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tools.invoke(tool_call)
    message.append(tool_msg)

print(message)
# print(model.invoke(message).content)
print(model_with_tool.invoke(message).content)