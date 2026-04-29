from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. 定义大模型
# 默认从环境变量读取
model = ChatOpenAI(
    model = "deepseek-chat",
    # temperature = 0, # 采样温度, 越高的随机性就越强,越发散
    # max_tokens = 10, # 最大tokens数
    # timeout = None,  # 超时时间
    # max_retries = 2, # 最大重试次数
    api_key = "sk-ac14cf3ae19045a091a1e9a8ae8925b1",# API Key
    base_url = "https://api.deepseek.com/v1",
    # organization = " "  # OpenAI 组织ID
)

# 2. 定义消息列表
messages = [
    SystemMessage(content = "请补全一段故事, 10个字以内"),
    HumanMessage(content = "一只猫正在__?")
]

response = model.invoke(messages)
print(response.response_metadata)  # 通常会包含 token 用量

# 3. 定义消息输出格式
parser = StrOutputParser()
# print(model.invoke(parser))

# 4. 定义链式, 链式来执行
chain = model | parser
print(chain.invoke(messages))