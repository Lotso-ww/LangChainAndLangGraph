from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_deepseek import ChatDeepSeek
from typing import Optional, List, Any, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

from LangChain.test21 import chain

model = ChatDeepSeek(model="deepseek-chat")
# 1. 定义结构化输出
# class Person(BaseModel):
#     """一个人的信息。"""
#
#     # 注意:
#     # 1. 每个字段都是 Optional “可选的” —— 允许 LLM 在不知道答案时输出 None。
#     # 2. 每个字段都有一个 description “描述” —— LLM使用这个描述。
#     # 有一个好的描述可以帮助提高提取结果。
#     name: Optional[str] = Field(default=None, description="这个人的名字")
#     hair_color: Optional[str] = Field(default=None, description="如果知道这个人头发的颜色")
#     skin_color: Optional[str] = Field(default=None, description="如果知道这个人的肤色")
#     height_in_meters: Optional[str] = Field(default=None, description="以米为单位的高度")
#
# class Data(BaseModel):
#     """人员信息列表"""
#     People: List[Person]
#
# structured_model = model.with_structured_output(schema=Data)
# messages = [
#     SystemMessage(content="你是一个提取信息的专家，只从文本中提取相关信息。如果您不知道要提取的属性的值，属性值返回null"),
#     HumanMessage(content="篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。")
# ]
# result = structured_model.invoke(messages)
# print(result)
#


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


# 2. 定义案例(还不是Message)
example = [
    (
        "海洋是广阔的, 蓝色的。它有两万多英尺深",
        Data(People=[]),
    ),
    (
        "小明在跳舞, 1米78的身高看起来很灵活",
        Data(People=[
            Person(name='小明', hair_color=None, skin_color=None, height_in_meters='1.78'),
        ]),
    ),
]

# 3. 定义提示词模版
prompt_template = ChatPromptTemplate(
    [
        SystemMessage(content="你是一个提取信息的专家，只从文本中提取相关信息。如果您不知道要提取的属性的值，属性值返回null"),
        MessagesPlaceholder("example_messages"), # 消息占位符, 将示例转换为message后插入进来
        ("user","new_message") # "篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。"
    ]
)

# 4. 将实例转换为Messages
example_messages = []

# 5. 定义的结构化模型
structured_model = model.with_structured_output(schema=Data)

# 6. 定义链
chain = prompt_template | structured_model
chain.invoke(
    {
        "example_messages": example_messages,
        "new_messages": "篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。",
    }
).pretty_print()