from langchain_core.tools import tool

# 定义工具
@tool
def add(a: int, b: int) -> int:
    """两数相加

    Args:
        a (int): a
        b (int): b
    """
    return a + b

print(add.invoke({"a" : 2, "b" : 3}))
print(add.name)
print(add.description)
print(add.args)