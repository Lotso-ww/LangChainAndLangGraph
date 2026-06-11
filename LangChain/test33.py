from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisVectorStore, RedisConfig

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