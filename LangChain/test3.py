from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy import result_tuple

# # 1. 基本用法
# # gpt_model = init_chat_model(model="gpt-4o-mini", model_provider="openai", temperature=0.3)
# deepseek_model = init_chat_model(model="deepseek-chat", model_provider="deepseek", temperature=0.3)
#
# # print(f"gpt-4o-mini: {gpt_model.invoke("你是谁").content}")
# print(f"deepseek-chat: {deepseek_model.invoke("你是谁").content}")


# # 2. 定义可配置的模型,模型模拟器
# config_model = init_chat_model(temperature=0.3)
# messages = [
#     SystemMessage(content = "请补全一段故事, 100个字以内"),
#     HumanMessage(content = "一只猫正在__?")
# ]
#
# # .invoke()的config参数才是真正意义上的定义了模型
# print(f"config_model: {config_model.invoke(input=messages, config={"configurable": {"model" : "deepseek-chat"}}).content}")

# 3. 可配置模型（带上默认值）
model = init_chat_model(
    model = "deepseek-chat",
    model_provider="deepseek",
    temperature = 0.3,
    max_tokens = 1024,
    # "max_tokens 后面还得再跟一个, "
    configurable_fields = ("max_tokens",),
    config_prefix = "first"
)

messages = [
    SystemMessage(content = "请补全一段故事, 100个字以内"),
    HumanMessage(content = "一只猫正在__?")
]

result = model.invoke(
    messages,
    config = {
        "configurable" : {
            "first_max_tokens" : 10,
        }
    }
)

print(result)