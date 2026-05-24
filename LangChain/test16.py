from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(model="deepseek-v4-flash")

# model.invoke("我是小明, 你好").pretty_print()
# model.invoke("你知道我是谁吗?").pretty_print()

# message = [
#     HumanMessage("我是小明, 你好"),
#     AIMessage("你好，小明！很高兴认识你。有什么我可以帮你的吗？"),
#     HumanMessage("你知道我是谁吗？")
# ]
#
# model.invoke(message).pretty_print()

store = {}
# 根据会话id查询会话中的消息列表
def get_session_history(session_id: str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_history_message_model = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id" : "1"}}
with_history_message_model.invoke(
    [HumanMessage("你好, 我是小明")],
    config=config
).pretty_print()

with_history_message_model.invoke(
    [HumanMessage("你知道我是谁吗?")],
    config=config
).pretty_print()