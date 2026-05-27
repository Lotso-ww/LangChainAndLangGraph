from langchain_deepseek import ChatDeepSeek
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage


model = ChatDeepSeek(model="deepseek-chat")

# 1. 定义结构化输出
class Person(BaseModel):
    """一个人的信息。"""

    # 注意:
    # 1. 每个字段都是 Optional “可选的” —— 允许 LLM 在不知道答案时输出 None。
    # 2. 每个字段都有一个 description “描述” —— LLM使用这个描述。
    # 有一个好的描述可以帮助提高提取结果。
    name: Optional[str] = Field(default=None, description="这个人的名字")
    hair_color: Optional[str] = Field(default=None, description="如果知道这个人头发的颜色")
    skin_color: Optional[str] = Field(default=None, description="如果知道这个人的肤色")
    height_in_meters: Optional[str] = Field(default=None, description="以米为单位的高度")

class Data(BaseModel):
    """人员信息列表"""
    People: List[Person]

structured_model = model.with_structured_output(schema=Data)
messages = [
    SystemMessage(content="你是一个提取信息的专家，只从文本中提取相关信息。如果您不知道要提取的属性的值，属性值返回null"),
    HumanMessage(content="篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。")
]
result = structured_model.invoke(messages)
print(result)