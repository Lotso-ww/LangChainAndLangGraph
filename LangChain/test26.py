from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader
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


# loader = PyPDFLoader(file_path="../DOC/PDF/QQMusic项目文档.pdf")
# docs = loader.load()
#
# # PDF加载器默认将文档按分页进行拆分
# print(f"PDF文档总页数：\n{len(docs)}\n")
# print(f"第一页文本的内容(前200)是：\n{docs[0].page_content[:200]}\n")
# print(f"第一页的元数据字典是：\n{docs[0].metadata}\n")
# print(f"第二页文本的内容(前200)是：\n{docs[1].page_content[:200]}\n")
# print(f"第二页的元数据字典是：\n{docs[1].metadata}\n")
#
# # PDF加载器将文本加载进来了，图片呢？
# print(f"第三页文本的内容(前200)是：\n{docs[2].page_content[:200]}\n")
# print(f"第三页的元数据字典是：\n{docs[2].metadata}\n")
# print(f"第三页：\n{docs[2]}\n")
#
# # PDF 文本 -》 Document -》 LLM
# # PDF 包含图片  -》 LLM (支持多模态)   # 直接将图片交给支持多模态的大模型处理可能是更加准确的！


# 文档加载器（MD）
md_loader = UnstructuredMarkdownLoader(
    "../Docs/markdown/脚手架级微服务租房平台Q&A.md",
    # mode="single",    # MD 加载器默认将文档加载为一个
    mode="elements",    # 拆分成不同类型的子块
)
# Document 列表
docs = md_loader.load()


print(f"MD文档总数：\n{len(docs)}\n")
print(f"第一个文档的内容是：\n{docs[0].page_content}\n")
# 'source': '../Docs/markdown/脚手架级微服务租房平台Q&A.md'
# 'category': 'Title',                              # 分类
# 'element_id': '3a0670f9bfd58576e430ef11def41593'  # 每个文档的唯一标识
print(f"第一个文档的元数据字典是：\n{docs[0].metadata}\n")

print(f"第二个文档的内容是：\n{docs[1].page_content}\n")
# 'source': '../Docs/markdown/脚手架级微服务租房平台Q&A.md'
# 'parent_id': '3a0670f9bfd58576e430ef11def41593',
# 'category': 'Title',
# 'element_id': 'fcb08b2a85942455eecebb9467ffca4c'
print(f"第二个文档的元数据字典是：\n{docs[1].metadata}\n")

print(f"第三个文档的内容是：\n{docs[2].page_content}\n")
# 'source': '../Docs/markdown/脚手架级微服务租房平台Q&A.md'
# 'parent_id': 'fcb08b2a85942455eecebb9467ffca4c',
# 'category': 'UncategorizedText',                    # 未分类文本
# 'element_id': 'a6fc0b5a457d21234bf1c4a6ae0a18db'
print(f"第三个文档的元数据字典是：\n{docs[2].metadata}\n")

# {
# 'Table',            表格
# 'Image',            图像
# 'NarrativeText',    叙事性文本
# 'Title',            标题
# 'ListItem',         列表项
# 'UncategorizedText' 未分类的文本
# }
print(f"当前MD文档的所有分类：{set(document.metadata["category"] for document in docs)}")