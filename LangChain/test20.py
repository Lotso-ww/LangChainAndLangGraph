from langchain_community.tools.playwright.base import lazy_import_playwright_browsers
from langchain_deepseek import ChatDeepSeek
from langsmith import Client
client = Client()
prompt = client.pull_prompt("hardkothari/prompt-maker")

model = ChatDeepSeek(model="deepseek-v4-flash")
chain = prompt | model

while True:
    task = input("\n 你的任务是什么? (输入 quit 退出聊天)\n")
    if task == "quit":
        break

    lazy_prompt = input("\n 你当前任务的对应提示词？(输入 quit 退出聊天)\n")
    if lazy_prompt == "quit":
        break

    chain.invoke({"task": task, "lazy_prompt": lazy_prompt}).pretty_print()
