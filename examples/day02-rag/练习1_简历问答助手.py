
import os
from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings
from openai.types.chat import ChatCompletionChunk
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

from pathlib import Path

#所有简历放在此处
resume_dir = Path("./resumes")


load_dotenv()
DB_PATH = "./my_pdf_db"

embeddings = DashScopeEmbeddings(
    model=os.getenv("AL_EM_MODE"),
    dashscope_api_key=os.getenv("AL_EM_KEY"),
)

from langchain_community.vectorstores import Chroma



if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )
    print(f"已加载本地向量库，共 {vectorstore._collection.count()} 条")
else:

    all_chunks = []
    for filepath in resume_dir.glob("*.pdf"):
        name = filepath.stem
        docs = PyPDFLoader(str(filepath)).load()
        for doc in docs:
            doc.metadata["person"] = name
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)
        print(f"{name}:{len(docs)} 页 -> {len(chunks)} 块")

    print(f"ALL_CHUNKS: {len(all_chunks)} 块")
    print(f"RESUME_DIR: {resume_dir.absolute()}, PDF数: {len(list(resume_dir.glob('*.pdf')))}")

    vectorstore = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    batch_size=10
    for i in range(0,len(all_chunks),batch_size):
        batch = all_chunks[i:i+batch_size]
        vectorstore.add_documents(batch)
        print(f"已存入{i+len(batch)}/{len(all_chunks)}")

    print(f"向量库已新建，共 {vectorstore._collection.count()} 条")


question = "你现在是一个简历助手，后续你会根据用户的简历来回答问题"

docs = vectorstore.similarity_search(question,k=5)

context = "\n\n".join(doc.page_content for doc in docs)
print("搜到的内容")
print(context)
print("===================")
prompt=f"""基于以下参考资料回答用户问题。
如果资料中没有相关信息，就说"我无法根据现有资料回答"，不要编造。

参考资料：
{context}

用户问题：{question}
回答："""



from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)




# 带着多轮回忆对话

chat_history = []   #存放之前的对话
print("=== 带记忆的 RAG 问答（输入 quit 退出）===\n")

while True:
    question = input("你：")
    if question.lower()=="quit":
        break

    # 1.搜向量库
    docs = vectorstore.similarity_search(question,k=3)
    context = "\n\n".join(doc.page_content for doc in docs)

    # 2.拼接历史对话
    history_text = ""
    for q,a in chat_history[-3:]:
        history_text += f"用户：{q}\nAI:{a}\n"

    # 3.拼 Prompt (多了历史对话)
    if history_text:
        prompt = f"""基于以下参考资料和历史对话回答用户问题。
                如果资料中没有相关信息，就说"我无法根据现有资料回答"，不要编造。

                参考资料：
                {context}

                历史对话：
                {history_text}
                用户问题：{question}
                回答："""
    else:
        # 第一轮没有历史，跟之前一样
        prompt = f"""基于以下参考资料回答用户问题。
                如果资料中没有相关信息，就说"我无法根据现有资料回答"，不要编造。

                参考资料：
                {context}

                用户问题：{question}
                回答："""

    # 调用LLM

    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=[
            {"role":"user","content":prompt}
        ],
        stream=True
    )

    print("AI: ",end="",flush=True)




    full_answer = ""
    for chunk in response:
        chunk: ChatCompletionChunk
        content = chunk.choices[0].delta.content
        if content:
            print(content,end="",flush=True)
            full_answer += content
    print("\n")

    chat_history.append((question,full_answer))
