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