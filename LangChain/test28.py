from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter


loader = UnstructuredMarkdownLoader(file_path="../DOC/md/脚手架级微服务租房平台Q&A.md")
data = loader.load()

# text_spliter = CharacterTextSplitter(
#     separator="\n\n",
#     chunk_size=400,
#     chunk_overlap=50,
#     length_function=len,
#     is_separator_regex=False,
# )
#
# documents = text_spliter.split_documents(data)
# for document in documents[:10]:
#     print("*" * 30)
#     print(document)


text_spliter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=400,
    chunk_overlap=50,
)

documents = text_spliter.split_documents(data)
for document in documents[:10]:
    print("*" * 30)
    print(document)