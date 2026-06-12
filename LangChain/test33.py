from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisVectorStore, RedisConfig
from langchain_text_splitters import CharacterTextSplitter

# 嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
)

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

# CRUD

# single 模式，只生成一个大文档
loader = UnstructuredMarkdownLoader("../Doc/md/脚手架级微服务租房平台Q&A.md",)
# Document 列表
data = loader.load()

# tiktoken 分词器
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", # cl100k_base 是tiktoken 分词器中的一种编码方式
    chunk_size=400,              # 块token大小(参考标准，为了保证段落/句子完整，会超出此设定的大小)
    chunk_overlap=50,            # 块重叠大小
)

# 文档列表
docs = text_splitter.split_documents(data)
for i, doc in enumerate(docs, start=1):
    doc.metadata["category"] = "QA"
    doc.metadata["num"] = i

# 编制索引 -- 添加文档
ids = vector_store.add_documents(docs)
print(f"编制了{len(ids)}个索引")
print(f"前三个索引是：{ids[:3]}")

# 查
# print(vector_store.get_by_ids(["01KTWNEF8M2E830475BCCYC61A"]))

# 删除
vector_store.delete(["01KTWNEF8M2E830475BCCYC61A"])
print(vector_store.get_by_ids(["01KTWNEF8M2E830475BCCYC61A"]))

# vector_store.index.drop_keys(["qa:01KTWNEF8M2E830475BCCYC61A"])

# 全量删除
# vector_store.index.delete(drop=True)
