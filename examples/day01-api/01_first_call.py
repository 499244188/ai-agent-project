"""
第一次调用 LLM API
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
        {"role": "user", "content": "介绍下你自己"}
    ]
)

print(response.choices[0].message.content)
