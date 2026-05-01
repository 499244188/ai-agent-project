"""
Day 2 - RAG 简历问答助手
把 PDF 简历存进向量库，用语义检索 + LLM 回答问题
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

DB_PATH = "./my_pdf_db"
resume_dir = Path("./resumes")

# Embedding（阿里 DashScope，不需要 PyTorch）
embeddings = DashScopeEmbeddings(
    model=os.getenv("AL_EM_MODE"),
    dashscope_api_key=os.getenv("AL_EM_KEY")
)

# 加载或新建向量库
if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    print(f"已加载本地向量库，共 {vectorstore._collection.count()} 条")
else:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []

    for filepath in resume_dir.glob("*.pdf"):
        name = filepath.stem
        docs = PyPDFLoader(str(filepath)).load()
        for doc in docs:
            doc.metadata["person"] = name
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)
        print(f"{name}: {len(docs)} 页 -> {len(chunks)} 块")

    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    batch_size = 10
    for i in range(0, len(all_chunks), batch_size):
        vectorstore.add_documents(all_chunks[i:i + batch_size])
    print(f"向量库已新建，共 {vectorstore._collection.count()} 条")

# DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

# 多轮对话
chat_history = []
print("=== 简历问答助手（输入 quit 退出）===\n")

while True:
    question = input("你：")
    if question.lower() == "quit":
        break

    # 1. 搜向量库
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 2. 拼历史对话
    history_text = ""
    for q, a in chat_history[-3:]:
        history_text += f"用户：{q}\nAI：{a}\n"

    # 3. 拼 Prompt
    if history_text:
        prompt = f"""基于以下参考资料和历史对话回答。
如果资料中没有相关信息，说"无法根据现有资料回答"。

参考资料：
{context}

历史对话：
{history_text}
用户问题：{question}
回答："""
    else:
        prompt = f"""基于以下参考资料回答。
如果资料中没有相关信息，说"无法根据现有资料回答"。

参考资料：
{context}

用户问题：{question}
回答："""

    # 4. 调 LLM（流式输出）
    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    print("AI: ", end="", flush=True)
    full_answer = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            full_answer += content
    print("\n")

    chat_history.append((question, full_answer))
