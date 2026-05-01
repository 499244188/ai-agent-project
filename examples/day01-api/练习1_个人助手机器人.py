"""
练习 1：多轮对话机器人
- System Prompt 设定身份
- 支持多轮对话（记住上下文）
- 流式输出
- 输入 quit 退出
"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

messages = []
messages.append({
    "role": "system",
    "content": "你是一个专注于AI Agent开发的学习助手。你必须始终以Agent开发导师的身份回答问题，回答时优先从Agent架构、工具调用、规划推理等角度出发。如果用户的问题偏离了Agent学习主题，请引导用户回到主题上。"
})

user_input = ""
while user_input.lower() != "quit":
    print("===== 输入 quit 退出 ========")
    user_input = input("你：")
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=os.getenv("DP_MODE"),
        messages=messages,
        stream=True,
        temperature=0.1
    )

    full_response = ""
    print("AI ==>:")
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content

    messages.append({"role": "assistant", "content": full_response})
