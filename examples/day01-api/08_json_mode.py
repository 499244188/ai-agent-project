"""
JSON Mode：让 AI 输出结构化 JSON
"""
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DP_API_KEY"),
    base_url=os.getenv("DP_URL")
)

response = client.chat.completions.create(
    model=os.getenv("DP_MODE"),
    messages=[
        {"role": "system", "content": """你是一个信息提取助手。
            从用户输入中提取信息，返回JSON格式。
            格式：{"name": "姓名", "age": 年龄, "city": "城市", "job": "职业"}
            如果信息缺失，对应字段填null"""
         },
        {"role": "user", "content": "我是小明，今年25了，在上海做写代码的牛马"}
    ],
    temperature=0.1,
    response_format={"type": "json_object"}
)

result_text = response.choices[0].message.content
print("原始回复：", result_text)

# 清理格式
if result_text.startswith("```json"):
    result_text = result_text[7:-3]
elif result_text.startswith("```"):
    result_text = result_text[3:-3]

result = json.loads(result_text)
print("解析结果:", result)
print("姓名：", result["name"])
print("城市：", result["city"])
print("工作：", result["job"])
