"""
流式输出：一个字一个字蹦出来
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[
        {"role": "user", "content": "请介绍下各个心理学之间的关系"}
    ],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print()
