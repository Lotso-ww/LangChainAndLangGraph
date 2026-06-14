from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_deepseek import ChatDeepSeek
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_text_splitters import CharacterTextSplitter

# 嵌入模型
embeddings = DashScopeEmbeddings(model="text-embedding-v3")
# 聊天模型
model = ChatDeepSeek(model="deepseek-chat")

# # single 模式，只生成一个大文档
# loader = UnstructuredMarkdownLoader("../Doc/md/脚手架级微服务租房平台Q&A.md",)
# # Document 列表
# data = loader.load()
#
# # tiktoken 分词器
# text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
#     encoding_name="cl100k_base", # cl100k_base 是tiktoken 分词器中的一种编码方式
#     chunk_size=400,              # 块token大小(参考标准，为了保证段落/句子完整，会超出此设定的大小)
#     chunk_overlap=50,            # 块重叠大小
# )
# # 文档列表
# docs = text_splitter.split_documents(data)
# Redis 配置
config = RedisConfig(
    index_name="qa",  # 定义索引名
    redis_url="redis://124.222.15.175:6379",
    metadata_schema=[
        {"name": "category", "type": "tag"},   # 添加索引字段：分类
        {"name": "num", "type": "numeric"},    # 添加索引字段：编号
    ]
)

# 初始化 Redis 向量存储实例（建立了索引结构）
vector_store = RedisVectorStore(
    embeddings=embeddings,
    config=config,
)
# 文档只需要添加一次即可
# vector_store.add_documents(docs)

# 检索器
retriever = vector_store.as_retriever()

# 提示词模版
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "human",
            """你是负责回答问题的助手,使用一下检索到的上下文片段来回答问题。如果你不知道答案，就直接说不知道。最多回复三句话的结果，回答要简明扼要
            Question:{question}
            Context:{context}
            Answer:"""
        )
    ]
)

# 将检索出来的文档转换成文本传递给提示词模版
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# for chunk in chain.stream("项目介绍"):
#     print(chunk, end="|", flush=True)
while True:
    # 获取用户输入
    question = input("\n请输入您的问题（输入'退出'或'quit'结束程序）: ").strip()

    # 检查是否退出
    if question.lower() in ["退出", "quit"]:
        print("程序已结束，再见！")
        break

    # 检查输入是否为空
    if not question:
        print("问题不能为空，请重新输入。")
        continue

    # 执行链，流式输出
    print("回答: ", end="", flush=True)
    for chunk in chain.stream(question):
        print(chunk, end="", flush=True)
    print()  # 换行