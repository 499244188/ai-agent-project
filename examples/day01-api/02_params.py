"""
API 参数：temperature、max_tokens、system prompt
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
        {"role": "system", "content": "你是一个专业的诗人"},
        {"role": "user", "content": "写一首关于失恋的五言绝句"}
    ],
    temperature=0.9,
    max_tokens=200,
    top_p=0.95,
    frequency_penalty=0.5
)

print(response.choices[0].message.content)
