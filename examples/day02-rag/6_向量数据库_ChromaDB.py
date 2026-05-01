

import chromadb

# 创建客户端
clinet = chromadb.PersistentClient(path='./dataset/chroma_db')

# 创建一个集合（类似数据库的表）
collection = clinet.get_or_create_collection(
    name="my_docs",
    metadata={"hnsw:space":"cosine"}  #用余弦相似度
)

# 添加文档
collection.add(
    documents=["Python是一种编程语言", "Java也是一种编程语言", "今天天气很好"],
    ids=["doc1","doc2","doc3"],
    metadatas=[
        {"source":"wiki"},
        {"source":"wiki"},
        {"source":"weather"},
    ]
)

# 查询
results = collection.query(
    query_texts=["程序"],
    n_results=3    # 返回最相似的两个
)

print("查询结果：程序")
for doc,dist in zip(results["documents"][0],results["distances"][0]):
    print(f"   文档：{doc} 相似度：{1-dist:.4f}")
