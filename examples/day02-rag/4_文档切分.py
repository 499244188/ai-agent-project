

from langchain_community.document_loaders import TextLoader

# 加载纯文本文件
loader = TextLoader("dataset/1.txt",encoding="utf-8")
docs = loader.load()


from langchain.text_splitter import RecursiveCharacterTextSplitter
# # 创建切分器
# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=50,
#     separators=["\n\n", "\n", "。", "！", "？", " ", ""]
# )

# chunks = splitter.split_documents(docs)

# print(f"原始文档： {len(docs)} 个")
# print(f"切分后：  {len(chunks)} 块")
# print(f"第二块 {chunks[1].page_content[:100]}...")




from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["。","！","？","\n","；"," ",""]
    # 中文优先用句号切分
)

chunks = splitter.split_documents(docs)

print(f"原始文档： {len(docs)} 个")
print(f"切分后：  {len(chunks)} 块")
print(f"第二块 {chunks[1].page_content[:1000]}...")
