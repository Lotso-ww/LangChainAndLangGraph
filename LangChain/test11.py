import asyncio

from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(model="deepseek-chat")

# print(model.invoke("写一篇关于春天从作文, 300字").content)

# # 同步流式传输
# chunks = []
# for chunk in model.stream("写一篇关于春天从作文, 300字"):
#     chunks.append(chunk)
#     # chunk: AIMessageChunk
#     print(chunk.content, end="|", flush=True)
#
# # 我们还可以看看相加
# # 加完后还是 AIMessageChunk
# # tmp_chunks = chunks[0] + chunks[1] + chunks[2] + chunks[3]
# # print(tmp_chunks)

# 异步流式输出
async def async_stream():
    print("====异步调用====")
    async for chunk in model.astream("写一篇关于春天从作文, 300字"):
        print(chunk.content, end="|", flush=True)

asyncio.run(async_stream())