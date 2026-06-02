from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from sqlalchemy.testing.suite.test_reflection import metadata

documents = [
    Document(
        page_content = "狗是我们最忠实的伙伴",
        metadata = {"source":"pets-doc"}
    ),
    Document(
        page_content="猫是我们最贴心的伙伴",
        metadata={"source": "pets-doc"}
    )
]


loader = PyPDFLoader(file_path="../DOC/PDF/QQMusic项目文档.pdf")
docs = loader.load()

# PDF加载器默认将文档按分页进行拆分
print(f"PDF文档总页数：\n{len(docs)}\n")
print(f"第一页文本的内容(前200)是：\n{docs[0].page_content[:200]}\n")
print(f"第一页的元数据字典是：\n{docs[0].metadata}\n")
print(f"第二页文本的内容(前200)是：\n{docs[1].page_content[:200]}\n")
print(f"第二页的元数据字典是：\n{docs[1].metadata}\n")

# PDF加载器将文本加载进来了，图片呢？
print(f"第三页文本的内容(前200)是：\n{docs[2].page_content[:200]}\n")
print(f"第三页的元数据字典是：\n{docs[2].metadata}\n")
print(f"第三页：\n{docs[2]}\n")

# PDF 文本 -》 Document -》 LLM
# PDF 包含图片  -》 LLM (支持多模态)   # 直接将图片交给支持多模态的大模型处理可能是更加准确的！