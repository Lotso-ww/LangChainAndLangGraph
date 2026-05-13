from typing import Optional, List

from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field


model = ChatDeepSeek(model="deepseek-chat")

# Pydantic 对象
class Joke(BaseModel):
    """讲的一个笑话"""
    setup: str = Field(description="这个笑话的开头")
    punchline: str = Field(description="这个笑话的妙语")
    rating: Optional[int] = Field(default=None, description="从1-10分, 给这个笑话的评分")

# 嵌套对象
class Data(BaseModel):
    """获取笑话的数据列表"""
    jokes: List[Joke]

model_with_structured = model.with_structured_output(Data)
print(model_with_structured.invoke("分别讲一个关于唱歌和跳舞的笑话"))
