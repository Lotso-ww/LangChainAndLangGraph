# 反义词示例合集
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import LengthBasedExampleSelector, SemanticSimilarityExampleSelector, \
    MaxMarginalRelevanceExampleSelector
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]

# 示例模版
example_prompt = PromptTemplate.from_template("Input: {input}\nOutput: {output}")

# # 示例选择器(长度)
# example_selector = LengthBasedExampleSelector(
#     examples=example,
#     example_prompt=example_prompt,
#     max_length=30,
#     # 用于获取字符串长度的函数，用于确定包含哪些示例。
#     # 如果没有指定，它是作为默认值提供的。
#     # 该函数返回一个整数，表示字符串中由换行符或空格分隔的“单词”数量
#     # get_text_length: Callable[[str], int] = lambda x: len(re.split("\n| ", x))
# )

# # 示例选择器(语义)
# example_selector = SemanticSimilarityExampleSelector.from_examples(
#     example,                                          # 示例集
#     # OpenAIEmbeddings(model="text-embedding-3-large"), # 使用嵌入模型的能力度量语义
#     Chroma,                                           # 存储向量：向量数据库
#     k=2,                                              # 生成示例的数量
# )

# 示例选择器(MMR)
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    example,                                          # 示例集
    # OpenAIEmbeddings(model="text-embedding-3-large"), # 使用嵌入模型的能力度量语义
    Chroma,                                           # 存储向量：向量数据库
    k=2,                                              # 生成示例的数量
)
# 少样本模版
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix = "给出每个输入的词的反义词",
    suffix = "Input: {adjective}\nOutput: ",
    input_variables=["adjective"],
)

print(few_shot_prompt.invoke({"adjective": "big"}).to_messages()[0].content)