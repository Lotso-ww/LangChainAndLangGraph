from typing import Iterator, List

from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from requests_toolbelt.utils.deprecated import find_pragma

model = ChatDeepSeek(model="deepseek-chat")

parser = StrOutputParser()

# 自定义输出解析器
def split_into_list(input: Iterator[str])->Iterator[List[str]]:
    buffer = ""
    for chunk in input:
        buffer += chunk
        # 遇到 。刷新
        while "。" in buffer:
            # 找到句号的位置
            stop_idnex = buffer.index("。")
            # yield 用于创造生成器
            yield [buffer[:stop_idnex].strip()]
            buffer = buffer[stop_idnex+1:]
    # for 循环结束, 如果还有多的字
    yield [buffer.strip()]

chain = model | parser | split_into_list

for chunk in chain.stream("写一篇关于爱情的歌词, 需要5句话, 每句话用句号隔开"):
    print(chunk, end="|", flush=True)