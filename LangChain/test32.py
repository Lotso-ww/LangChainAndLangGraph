import redis
redis_url = "redis://124.222.15.175:6379"
# 定义Redis客⼾端
redis_client = redis.from_url(redis_url)
# Ping
print(redis_client.ping())