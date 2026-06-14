from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_deepseek import ChatDeepSeek
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_text_splitters import CharacterTextSplitter

# ==========================================
# 1. 模型初始化配置
# ==========================================
# 嵌入模型：用于将文本转换为向量表示，这里使用的是阿里云大模型的通用文本向量模型
embeddings = DashScopeEmbeddings(model="text-embedding-v3")
# 聊天模型：用于根据检索到的上下文生成最终回答，这里使用的是 DeepSeek 的对话模型
model = ChatDeepSeek(model="deepseek-chat")


# ==========================================
# 2. 文档加载与切割（离线数据准备阶段）
# 注：这部分当前被注释掉了，因为向量入库通常只需要执行一次。
# ==========================================
# # single 模式，只生成一个大文档
# loader = UnstructuredMarkdownLoader("../Doc/md/脚手架级微服务租房平台Q&A.md",)
# # 将 Markdown 文件加载为 Document 对象的列表
# data = loader.load()
#
# # 文本切割器：将长文档切分为更小的文本块（Chunk），以便于向量化和更精准的检索
# # 使用 tiktoken 分词器（OpenAI开源），按 token 数量而非字符数量进行切割
# text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
#     encoding_name="cl100k_base", # cl100k_base 是tiktoken 分词器中的一种编码方式
#     chunk_size=400,              # 每个文本块期望的最大 token 大小(为保证段落完整，实际可能略超)
#     chunk_overlap=50,            # 相邻文本块之间重叠的 token 数量，防止切断上下文关联
# )
# # 执行切割，得到适合入库的文档片段列表
# docs = text_splitter.split_documents(data)


# ==========================================
# 3. 向量数据库配置与初始化
# ==========================================
# Redis 配置：定义连接信息及向量库的元数据结构
config = RedisConfig(
    index_name="qa",  # 定义 Redis 中的索引名称，检索时会在该索引下查找
    redis_url="redis://124.222.15.175:6379", # Redis 服务的连接地址
    metadata_schema=[
        # 定义元数据字段，便于后续可以进行过滤检索（如只查某个分类）
        {"name": "category", "type": "tag"},   # 添加索引字段：分类
        {"name": "num", "type": "numeric"},    # 添加索引字段：编号
    ]
)

# 初始化 Redis 向量存储实例（如果索引不存在则会自动建立索引结构）
vector_store = RedisVectorStore(
    embeddings=embeddings, # 指定用于计算向量的嵌入模型
    config=config,         # 应用上面的 Redis 配置
)

# 将切割好的文档片段转换为向量并存入 Redis
# 文档只需要添加一次即可，所以这里注释掉了，避免重复运行代码时重复入库
# vector_store.add_documents(docs)

# 检索器：将向量数据库转换为一个可以用于检索的接口
retriever = vector_store.as_retriever()


# ==========================================
# 4. 提示词与处理链路 (LCEL 语法)
# ==========================================
# 提示词模版：告诉大模型它的角色，以及如何使用上下文（Context）和问题（Question）
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

# 辅助函数：将检索器返回的多个 Document 对象拼接成纯文本字符串，传给大模型的 {context} 变量
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 构建处理链 (Chain)：这是 LangChain 的核心概念，数据从上到下流转
chain = (
    # 步骤1：组装输入参数。
    # - context: 把用户的问题传给检索器(retriever)，将查到的文档通过 format_docs 转为文本。
    # - question: 用户输入的问题直接透传 (RunnablePassthrough)。
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    # 步骤2：将组装好的字典填入到提示词模版中
    | prompt
    # 步骤3：将填充好的提示词发送给 DeepSeek 模型进行推理生成
    | model
    # 步骤4：将大模型返回的复杂对象（AIMessage）解析为普通的字符串文本
    | StrOutputParser()
)


# ==========================================
# 5. 用户交互入口 (多轮问答的控制台交互)
# ==========================================
# 单次测试代码（已注释）
# for chunk in chain.stream("项目介绍"):
#     print(chunk, end="|", flush=True)

# 开启一个无限循环，提供持续的问答体验
while True:
    # 获取用户输入并去除首尾空格
    question = input("\n请输入您的问题（输入'退出'或'quit'结束程序）: ").strip()

    # 检查是否触发出行条件
    if question.lower() in ["退出", "quit"]:
        print("程序已结束，再见！")
        break

    # 检查输入是否为空（防止回车误触报错）
    if not question:
        print("问题不能为空，请重新输入。")
        continue

    # 执行链，并使用 stream 方法实现流式输出（打字机效果），提升用户体验
    print("回答: ", end="", flush=True)
    # chunk 是大模型每次生成的零碎文本片段
    for chunk in chain.stream(question):
        # end="" 保证输出不换行，flush=True 保证内容立即刷新到控制台
        print(chunk, end="", flush=True)
    print()  # 当整段回答输出完毕后，打印一个空行，为了美观