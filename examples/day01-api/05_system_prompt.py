"""
System Prompt：同一个问题，不同角色回答
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

system_prompts = [
    "你是一个五岁的小孩，用童言童语解释一切",
    "你是一个严格的教授，用学术语言严格地回答问题",
    "你是一个搞笑的脱口秀演员，用幽默的方式回答问题"
]

question = "什么是数据库"

for sp in system_prompts:
    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=[
            {"role": "system", "content": sp},
            {"role": "user", "content": question}
        ],
        temperature=0.7
    )
    print(f"角色：{sp[:10]}...")
    print(f"回复：{response.choices[0].message.content}\n")
    print("---\n")
