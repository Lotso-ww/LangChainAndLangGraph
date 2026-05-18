from langchain_deepseek import ChatDeepSeek

model = ChatDeepSeek(model="deepseek-chat")

# print(model.invoke("写一篇关于春天从作文, 300字").content)

# 流式传输
chunks = []
for chunk in model.stream("写一篇关于春天从作文, 300字"):
    chunks.append(chunk)
    # chunk: AIMessageChunk
    print(chunk.content, end="|", flush=True)

# 我们还可以看看相加
# 加完后还是 AIMessageChunk
# tmp_chunks = chunks[0] + chunks[1] + chunks[2] + chunks[3]
# print(tmp_chunks)