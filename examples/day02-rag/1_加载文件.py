
# # 加载txt
# from langchain_community.document_loaders import TextLoader

# # 加载纯文本文件
# loader = TextLoader("dataset/1.txt",encoding="utf-8")
# docs = loader.load()

# print(f"加载了{len(docs)} 个文档")
# print(f"内容预览：{docs[0].page_content[:200]}")
# print(f"元数据：{docs[0].metadata}")


# # 加载pdf

# from langchain_community.document_loaders import PyPDFLoader

# # 加载pdf(自动按页分割)
# loader = PyPDFLoader("./dataset/1.pdf")
# docs =loader.load()

# print(f"PDF共{len(docs)} 页")
# for i,doc in enumerate(docs):
#     print(f"第{i+1} 页：{doc.page_content[:100]}...")

# 加载markdown 文件

from langchain_community.document_loaders import UnstructuredMarkdownLoader
loader = UnstructuredMarkdownLoader("./dataset/1.md")
docs = loader.load()

print(len(docs))
print(type(docs))
