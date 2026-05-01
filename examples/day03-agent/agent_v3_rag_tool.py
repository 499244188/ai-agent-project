"""
Day 3 - Agent v3：RAG 变成工具 + 对话记忆
把向量检索包装成 Agent 的一个工具，LLM 自己决定搜不搜、搜什么、搜几轮
"""
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv()

# DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

# 阿里 Embedding
embeddings = DashScopeEmbeddings(
    model=os.getenv("AL_EM_MODE"),
    dashscope_api_key=os.getenv("AL_EM_KEY")
)

# 加载已有的向量库
vectorstore = Chroma(
    persist_directory="./my_pdf_db",
    embedding_function=embeddings
)

print(f"向量库加载成功，里面有 {vectorstore._collection.count()} 个文档块")

# ========== 工具定义 ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_resumes",
            "description": "搜索简历库，查找候选人信息。如果第一次搜不到完整信息，换关键词再搜。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "person": {
                        "type": "string",
                        "description": "可选，按人名过滤，如'张明辉'"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def search_resumes(query, person=None):
    if person:
        docs = vectorstore.similarity_search(query, k=3, filter={"person": person})
    else:
        docs = vectorstore.similarity_search(query, k=5)

    return "\n\n".join(
        f"[来源: {d.metadata.get('person', '未知')}]\n{d.page_content}"
        for d in docs
    )

tool_map = {"search_resumes": search_resumes}

# ========== Agent 循环 + 对话记忆 ==========
system_prompt = """你是一个简历搜索助手。你能帮用户在简历库中查找候选人信息。
当用户问关于候选人的问题时，使用 search_resumes 工具搜索。
如果第一次搜索结果不完整，可以换关键词再搜。
回答时注明来源是哪位候选人。"""

messages = [{"role": "system", "content": system_prompt}]

print("简历搜索 Agent（输入 quit 退出）\n")

while True:
    question = input("你：")
    if question.lower() == "quit":
        break

    messages.append({"role": "user", "content": question})

    for round_num in range(5):
        response = client.chat.completions.create(
            model=os.getenv("DP_MODE"),
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"  调用: {func_name}({func_args})")
                result = tool_map[func_name](**func_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        elif message.content:
            print(f"Agent: {message.content}\n")
            break
