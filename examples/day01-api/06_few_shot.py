"""
Few-shot：通过例子教 AI 输出固定格式
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
    {"role": "system", "content": "你是一个情感分析助手，判断用户评论的情感。只输出JSON格式。"},

    # 示例 1
    {"role": "user", "content": "这个手机太好用了，拍照清晰，电池耐用！"},
    {"role": "assistant", "content": '{"sentiment": "positive", "confidence": 0.95, "keywords": ["好用", "清晰", "耐用"]}'},

    # 示例 2
    {"role": "user", "content": "快递太慢了，包装还破了，差评！"},
    {"role": "assistant", "content": '{"sentiment": "negative", "confidence": 0.92, "keywords": ["慢", "破", "差评"]}'},

    # 示例 3
    {"role": "user", "content": "还行吧，一般般，没什么特别的"},
    {"role": "assistant", "content": '{"sentiment": "neutral", "confidence": 0.75, "keywords": ["一般", "没什么特别"]}'},

    # 现在问一个新的（AI 会模仿上面的格式）
    {"role": "user", "content": "性价比很高，就是外观丑了点"},
]

response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=messages,
    temperature=0.1
)

print(response.choices[0].message.content)
