from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(model="deepseek-chat")

# 案例: 参数
example = [
    {"text":"hi,what is your name?","output":"你好,你的名字是什么?"},
    {"text":"hi,what is your age?","output":"你好, 你的年龄是多少?"}
]

example_prompt = ChatPromptTemplate(
    [
        ("user", "{text}"),
        ("ai", "{output}"),
    ]
)

few_prompt = FewShotChatMessagePromptTemplate(
    examples=example,
    example_prompt=example_prompt,
)

# 最终提示词模版
chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个专业的翻译助手，不要输出任何额外内容, 你的工作就是翻译, 将文本从{language_from}翻译为{language_to}"),
        # 少样本示例
        few_prompt,
        ("user", "{text}")
    ]
)

# print(chat_prompt_template.invoke(
#     {
#         "language_from": "英文",
#         "language_to": "中文",
#         "text": "hi, what is your favorite food?",
#     }
# ))

chain = chat_prompt_template | model
chain.invoke(
    {
        "language_from": "英文",
        "language_to": "中文",
        "text": "hi, what is your favorite food?",
    }
).pretty_print()