from langchain_core.messages import HumanMessage
from langchain_deepseek import ChatDeepSeek
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
import datetime

from pydantic import BaseModel


model = ChatDeepSeek(model="deepseek-chat")

tools = TavilySearch(max_results=4)

model_with_tool = model.bind_tools([tools])

today = datetime.date.today()
message = [
    HumanMessage(f"今天是 {today}。请直接调用搜索工具查询武汉实时天气，并详细汇报")
]

ai_message = model_with_tool.invoke(message)
message.append(ai_message)

for tool_call in ai_message.tool_calls:
    tool_message = tools.invoke(tool_call)
    message.append(tool_message)

class SearchResult(BaseModel):
    """结构化搜索对象"""

    query: str = Field(description="搜索查询")
    findings: str = Field(description="查询结果摘要")

model_with_structured = model_with_tool.with_structured_output(SearchResult)
print(model_with_structured.invoke(message))