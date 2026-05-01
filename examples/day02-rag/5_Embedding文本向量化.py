# from langchain_openai import OpenAIEmbeddings

# embeddings = OpenAIEmbeddings(
#     model="text-embedding-ada-002",
#     openai_api_key=""
#     openai_api_base="https://api.deepseek.com""
# )


# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# load_dotenv()

# input_text = "衣服的质量非常的好"
# x = os.getenv("AL_EM_URL")

# client = OpenAI(
#     api_key = os.getenv("AL_EM_KEY"),
#     base_url =os.getenv("AL_EM_URL")
# )

# completion = client.embeddings.create(
#     model=os.getenv("AL_EM_MODE"),
#     input=input_text,
#     dimensions=64
# )


# data = completion.model_dump_json()
# print(type(data))



# from dotenv import load_dotenv
# load_dotenv()
# import os
# from langchain_openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(
#     model=os.getenv("AL_EM_MODE"),
#     openai_api_key=os.getenv("AL_EM_KEY"),
#     openai_api_base=os.getenv("AL_EM_URL")
# )
# # 把文字变成向量
# vector = embeddings.embed_query("什么是Python？")
# print(f"向量维度: {len(vector)}")
# print("前5个数字:", vector[:5])


from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings(
    model=os.getenv("AL_EM_MODE"),
    dashscope_api_key=os.getenv("AL_EM_KEY")
)

vector = embeddings.embed_query("什么是Python？")
print(vector)
# print(f"向量维度: {len(vector)}")
