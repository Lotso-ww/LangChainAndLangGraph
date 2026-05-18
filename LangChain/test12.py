import asyncio

from sqlalchemy.util import await_only
from tenacity import sleep


# # 同步IO
# def boil_water():
#     print("开始烧水")
#     sleep(5)
#     print("水烧开了")
#
# def send_message():
#     print("开始发消息")
#     sleep(2)
#     print("消息发完了")
#
# def main():
#     # 1. 烧水
#     boil_water()
#     # 2. 发消息
#     send_message()
#
# # 总共耗时 7s
# main()


# 异步IO
# 协程
async def boil_water_async():
    print("开始烧水")
    await asyncio.sleep(5)
    print("水烧开了")

# 协程
async def send_message_async():
    print("开始发消息")
    await asyncio.sleep(2)
    print("消息发完了")

# 协程
# 事件循环
async def main():
    # 1. 烧水
    task1 = asyncio.create_task(boil_water_async())
    # 2. 发消息
    task2 = asyncio.create_task(send_message_async())
    await task1
    await task2

# 总共耗时 5s
asyncio.run(main())