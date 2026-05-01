"""
多轮对话：手动维护 messages 列表
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

messages = [
    {"role": "system", "content": "你是一个很棒的物理老师，请用通俗易懂的语言解释"}
]

print("========= 物理老师对话 (输入 quit 退出) ========\n")

while True:
    user_input = input("你: ")
    if user_input.lower() == "quit":
        print("再见")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=messages
    )

    reply = response.choices[0].message.content
    print(f"老师: {reply}\n")

    messages.append({"role": "assistant", "content": reply})
