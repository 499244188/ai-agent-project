
import os
from dotenv import load_dotenv
# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import DashScopeEmbeddings
from openai.types.chat import ChatCompletionChunk


load_dotenv()
DB_PATH = "./my_psychology_db"

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
    knowledge_texts = [
        # 各学派定义
        "认知心理学研究人的思维过程，包括感知、记忆、语言和问题解决",
        "行为主义心理学强调可观察的行为，代表人物有斯金纳和华生",
        "精神分析学派由弗洛伊德创立，关注无意识对行为的影响",
        "人本主义心理学由马斯洛和罗杰斯提出，强调人的自我实现",
        # 关系（新增）
        "认知心理学和行为主义的分歧在于：是否研究内部心理过程",
        "人本主义心理学是在反对行为主义和精神分析的基础上发展起来的，被称为心理学第三势力",
        "四大心理学流派按时间顺序：精神分析→行为主义→人本主义→认知心理学，后者往往是对前者的批判和补充",
        ]

    # 每条给一个唯一 id，防止重复跑时数据叠加
    vectorstore = Chroma.from_texts(
        texts=knowledge_texts,
        embedding=embeddings,
        persist_directory=DB_PATH,
        ids=[f"psych_{i}" for i in range(len(knowledge_texts))]
    )
    print("向量库已新建")



question = "请介绍下各个心理学之间的关系"

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


# response = client.chat.completions.create(
#     model=os.getenv("DP_MODE"),
#     messages=[
#         {"role":"user","content":prompt}
#     ],
#     stream=True
# )

# print("\n AI 回答")

# for chunk in response:
#     content = chunk.choices[0].delta.content
#     if content:
#         print(content,end="",flush=True)

# print()


# 带着多轮回忆对话

chat_history = []   #存放之前的对话
print("=== 带记忆的 RAG 问答（输入 quit 退出）===\n")

while True:
    question = input("你：")
    if question.lower=="quit":
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
