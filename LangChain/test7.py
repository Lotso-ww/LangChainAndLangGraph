from langchain_core.messages import HumanMessage
from langchain_deepseek import ChatDeepSeek
from langchain_tavily import TavilySearch
import datetime


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

print(model_with_tool.invoke(message).content)
