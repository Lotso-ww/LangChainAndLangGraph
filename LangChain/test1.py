from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek

# 1. 定义大模型
# 默认从环境变量读取
model = ChatDeepSeek(model = "deepseek-reasoner")


# 2. 定义消息列表
# 系统提示消息: SystemMessage, 一般作为第一条消息传入
# 用户消息: HumanMessage
messages = [
    SystemMessage(content = "请帮我进行翻译, 从英文变成中文"),
    HumanMessage(content = "my name is XiaoMing")
]

# 3. 调用大模型(如果后面用链式的话这里就不需要先调用了)
# 我们这里如果调试可以看出来是个AI消息类型
# result = model.invoke(messages)
# print(result)

# 4. 定义消息输出格式
parser = StrOutputParser()
# print(model.invoke(parser))

# 5. 定义链式, 链式来执行
chain = model | parser
print(chain.invoke(messages))